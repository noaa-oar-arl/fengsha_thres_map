## README

### FV3 Threshold Map (make_map.py)

This is a small set of utilities to create a 2d maps based on the inputs of the FV3 FENGSHA dust emission model. Inputs for the program is the directory for of the FV3-CHEM emissions and the threhold values for the 12 category soil types.

```
./make_map.py --help
usage: make_map.py [-h] -d DATA_DIRECTORY -ut THRESHOLD_VELOCITY
                   [-r RESOLUTION]

generate fv3 chem threshold friction velocities

optional arguments:
  -h, --help            show this help message and exit
  -d DATA_DIRECTORY, --data_directory DATA_DIRECTORY
                        path to the emission data (for single month: i.e.
                        emi_C384/01) (default: None)
  -ut THRESHOLD_VELOCITY, --threshold_velocity THRESHOLD_VELOCITY
                        Threshold friction Velocity for soil types. Enter as
                        string: "0.065,0.18,0.28,0.30,0.35,0.45,0.45,0.42,0.42
                        ,0.45,0.50,0.45,9999.0" (default: 0.065,0.18,0.28,0.30
                        ,0.35,0.45,0.45,0.42,0.42,0.45,0.50,0.45,9999.0)
  -r RESOLUTION, --resolution RESOLUTION
                        FV3 Resolution: C384, C96, etc... (default: C384)
```

### Modify Lat lon box (modify_latlon_box.py)

Much like `make_map.py`, `modify_latlon_box.py` will modify the thresholds in a given latitude and longitude box to provide a regional application of threshold values.

```
./modify_latlon_box.py --help
usage: modify_latlon_box.py [-h] -d DATA_DIRECTORY -ut THRESHOLD_VELOCITY -b
                            LATLON_BOX [-o OUTPUT_FILENAME] [-r RESOLUTION]

Modify thresholds in a certain area

optional arguments:
  -h, --help            show this help message and exit
  -d DATA_DIRECTORY, --data_directory DATA_DIRECTORY
                        path to the emission data (for single month: i.e.
                        emi_C384/01) (default: None)
  -ut THRESHOLD_VELOCITY, --threshold_velocity THRESHOLD_VELOCITY
                        Threshold friction Velocity for soil types. Enter as
                        string: "0.065,0.18,0.28,0.30,0.35,0.45,0.45,0.42,0.42
                        ,0.45,0.50,0.45,9999.0" (default: 0.065,0.18,0.28,0.30
                        ,0.35,0.45,0.45,0.42,0.42,0.45,0.50,0.45,9999.0)
  -b LATLON_BOX, --latlon_box LATLON_BOX
                        Lat Lon box to modify threshold values: Lon min, lat
                        min, lon max, lat max (default: None)
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        output file name (default: uthr.dat)
  -r RESOLUTION, --resolution RESOLUTION
                        FV3 Resolution: C384, C96, etc... (default: C384)
                        ```
