#!/usr/bin/env python
import os
from numpy import array, arange
from scipy.io import FortranFile
import argparse
import monet as m
import xarray as xr
try:
    import fv3grid as fg
    has_fv3grid = True
except ImportError:
    has_fv3grid = False

def wrap_longitudes(lons):
    return (lons + 180) % 360 - 180

def open_fv3_binary(fname, dtype='f4', res='C384', tile=1):
    """Reads the binary data for FV3-CHEM input generated by prep_chem_sources.
    Parameters
    ----------
    fname : type
        Description of parameter `fname`.
    **kwargs :
        This is the kwargs for the fv3grid. Users can define the res='C384' and
        the tile=1.
        valid values for them are:
        res = 'C768' 'C384' 'C192' 'C96' 'C48'
        tile = 1 2 3 4 5 6
    Returns
    -------
    xaray DataArray
        Description of returned object.
    """
    w = FortranFile(fname)
    a = w.read_reals(dtype=dtype)
    w.close()
    r = int(res[1:])
    s = a.reshape((r, r), order='F')
    if has_fv3grid:
        grid = fg.get_fv3_grid(res=res, tile=tile)
#        print(grid)
        lons = wrap_longitudes(grid.longitude)
        grid['longitude'] = lons
#        grid['latitude'] = grid.latitude.T
        name = os.path.basename(fname).split('.dat')[0].split('.bin')[0]
        #name = fname.split('.bin')[0]
        grid[name] = (('x', 'y'), s)
        return grid
    else:
        print(
            'Please install the fv3grid from https://github.com/bbakernoaa/fv3grid'
        )
        print('to gain the full capability of this dataset')
        return xr.DataArray(s, dims=('x', 'y'))

def to_prepchem_binary(data, fname='output.bin', dtype='f4'):
    """Writes to binary file for prep_chem_sources.
    Parameters
    ----------
    dset : data array
        Description of parameter `dset`.
    fname : type
        Description of parameter `fname`.
    dtype : type
        Description of parameter `dtype`.
    Returns
    -------
    type
        Description of returned object.
    """
    f = FortranFile(fname, 'w')
    f.write_record(data.astype(dtype))
    f.close()

def patch_thres(uth,bedrock):
    from numpy import zeros, shape, arange,where
    return uth.where(bedrock > 0,999).data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Modify thresholds in a certain area',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--data_directory',
                        default=None,
                        required=True,
                        help='path to the emission data (for single month: i.e. bsmfv3)')
    parser.add_argument('-o', '--output_filename',
                        default='uthr.dat',
                        required=False,
                        help='output file name')
    parser.add_argument('-r','--resolution',
                        default='C384',
                        help='FV3 Resolution: C384, C96, etc...')
    args = parser.parse_args()

    d = os.path.abspath(args.data_directory)
    #thres = array(args.threshold_velocity.split(','),dtype=float)
    res = args.resolution
    output_fname = args.output_filename


    print('----------------------------------------------------')
    print(' Beginning program' )
    for i in arange(1,7):
        tile = 'tile{}'.format(int(i))
        #form full path of files
        uthres = os.path.join(d, tile, 'uthr.dat')
        output = os.path.join(d, tile, output_fname)
        print('Creating threshold data for {}'.format(tile))
        # open clay and sand
        print('     Opening Threshold...')
        uth = open_fv3_binary(uthres, res=res, tile=i).uthr
        bedrock = xr.open_dataset('ISRIC_BEDROCK_CMG.nc').bedrock
        b = uth.monet.remap_nearest(bedrock).load().astype(bool)
        th = patch_thres(uth, b)
        print('     Output: {}'.format(output))
        to_prepchem_binary(th.T,fname=output)
