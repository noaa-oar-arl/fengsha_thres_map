#!/bin/bash

for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
    
    thres="0.065,0.18,0.27,0.30,0.35,0.38,0.45,0.41,0.41,0.45,0.50,0.45,9999.0"
    #directory=/gpfs/hps3/emc/naqfc/noscrub/Barry.Baker/emissions/emi_LIPAN_C384/${month}
    directory=emi_C384/${month}
    ./make_map.py -ut $thres -d $directory
    
    # MODIFY AUS
    thres="0.065,0.18,0.38,0.30,0.35,0.38,0.55,0.41,0.41,0.45,0.50,0.45,9999.0"

    box="108,-40,154,-11"
    
    ./modify_latlon_box.py -ut $thres -d $directory -b $box
    
    # MODIFY TAKLAMAKAN
    
    thres="0.065,0.18,0.23,0.30,0.35,0.38,0.45,0.41,0.41,0.45,0.50,0.45,9999.0"
    box="77.6,36,89,41.1"
    
    ./modify_latlon_box.py -ut $thres -d $directory -b $box
    
done
