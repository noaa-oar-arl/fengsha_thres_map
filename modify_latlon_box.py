#!/usr/bin/env python
import os
from numpy import array, arange
from scipy.io import FortranFile
import argparse

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
    
def calc_soil_type(clay,sand,silt):
    from numpy import zeros,where
    stype = zeros(clay.shape)
    stype[where((silt + clay*1.5 < 15.) & (clay != 255))] = 1.  #SAND
    stype[where((silt + 1.5*clay >= 15.) & (silt + 1.5*clay <30) & (clay != 255))] = 2. #Loamy Sand
    stype[where((clay >= 7.) & (clay < 20) & (sand >52) & (silt + 2* clay >=30) & (clay != 255))] = 3. #Sandy Loam (cond 1)
    stype[where((clay <   7) & (silt < 50) & (silt+2*clay >= 30) & (clay != 255))]   = 3      # sandy loam (cond 2)
    stype[where((silt >= 50) & (clay >= 12) & (clay < 27 ) & (clay != 255))] = 4      # silt loam (cond 1)
    stype[where((silt >= 50) & (silt < 80) & (clay < 12) & (clay != 255))] = 4      # silt loam (cond 2)
    stype[where((silt >= 80) & (clay < 12) & (clay != 255))]     = 5      # silt
    stype[where((clay >= 7 ) & (clay < 27) &(silt >= 28) & (silt < 50) & (sand <= 52) & (clay != 255))] = 6      # loam
    stype[where((clay >= 20) & (clay < 35) & (silt < 28) & (sand > 45) & (clay != 255))] = 7      # sandy clay loam
    stype[where((clay >= 27) & (clay < 40.) & (sand < 20) & (clay != 255))] =  8      # silt clay loam
    stype[where((clay >= 27) & (clay < 40.) & (sand >= 20) & (sand <= 45) & (clay != 255))] = 9      # clay loam
    stype[where((clay >= 35) & (sand > 45) & (clay != 255))] = 10     # sandy clay
    stype[where((clay >= 40) & (silt >= 40) & (clay != 255))] = 11     # silty clay
    stype[where((clay >= 40) & (sand <= 45) & (silt < 40) & (clay != 255))] = 12     # clay
    return stype

def patch_thres(stype,uth,thresholds,loc_con):
    from numpy import zeros, shape, arange,where
    u = uth.data.copy()
    for i in arange(1,14):
#        print(i,thresholds[int(i)-1])
        u[where((loc_con) & (stype == i))] = thresholds[int(i)-1]
    return u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='download and gridding MODIS data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--data_directory',
                        default=None,
                        required=True,
                        help='path to the emission data (for single month: i.e. emi_C384/01)')
    parser.add_argument('-ut', '--threshold_velocity',
                        default="0.065,0.18,0.28,0.30,0.35,0.45,0.45,0.42,0.42,0.45,0.50,0.45,9999.0",
                        required=True,
                        help='Threshold friction Velocity for soil types.  Enter as string: "0.065,0.18,0.28,0.30,0.35,0.45,0.45,0.42,0.42,0.45,0.50,0.45,9999.0"')
    parser.add_argument('-b', '--latlon_box',
                        default=None,
                        required = True,
                        help='Lat Lon box to modify threshold values: Lon min, lat min, lon max, lat max')
    parser.add_argument('-o', '--output_filename',
                        default='uthr.dat',
                        required=False,
                        help='output file name')
    parser.add_argument('-r','--resolution',
                        default='C384',
                        help='FV3 Resolution: C384, C96, etc...')
    args = parser.parse_args()

    d = os.path.abspath(args.data_directory)
    thres = array(args.threshold_velocity.split(','),dtype=float)
    res = args.resolution
    output_fname = args.output_filename
    lonmin,latmin,lonmax,latmax = array(args.latlon_box.split(','),dtype=float)

    for i in arange(1,7):
        tile = 'tile{}'.format(int(i))
        #form full path of files
        clay_file = os.path.join(d, tile, 'clay.dat')
        sand_file = os.path.join(d, tile, 'sand.dat')
        uthres = os.path.join(d, tile, 'uthr.dat')
        output = os.path.join(d, tile, output_fname)
        print('Creating threshold data for {}'.format(tile))
        # open clay and sand
        print('     Opening Threshold...')
        uth = open_fv3_binary(uthres, res=res, tile=i).uthr
        loc_con = (uth.longitude.T > lonmin) & (uth.latitude.T > latmin) & (uth.longitude.T < lonmax) & (uth.latitude.T < latmax)
        #        if loc_con.max() == False:
        #            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #            print('   Lat Lon Box not in {}'.format(tile))
        #            print('   Copying uthr.dat to {}'.format(output_fname))
        #            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #            to_prepchem_binary(uth.data,fname=output)
        #        else:
        print('     Opening Clay...')
        clay = open_fv3_binary(clay_file, res=res, tile=i).clay
        print('     Opening Sand...')
        sand = open_fv3_binary(sand_file, res=res, tile=i).sand
        # calculate silt from sand and clay
        #( 1 = clay + sand + silt)
        silt = 1 - clay - sand
        # needs % multiply by 100
        print('     Caclulating Soil Type...')
        stype = calc_soil_type(clay*100,sand*100,silt*100)
        st = clay.copy()
        st.data = stype
        print('     Setting Thresholds...')
        th = patch_thres(stype,uth,thres,loc_con)
        print('     Output: {}'.format(output))
        to_prepchem_binary(th.T,fname=output)
            
        
        
