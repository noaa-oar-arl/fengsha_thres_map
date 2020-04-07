#!/bin/bash

#------------------------Set these here -------------
res='C384'
#res='C96'
#base_dir=emi_C96
base_dir=/gpfs/dell2/emc/modeling/noscrub/Barry.Baker/emi_C384/fengsha

#----------------------------------------------------
#for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
for month in 03; do

    echo "SETTING DEFAULT THRESHOLDS"
    thres="0.065,0.18,0.23,0.30,0.35,0.38,0.45,0.41,0.41,0.45,0.50,0.45,9999.0"
     directory=${base_dir}/${month}
    ./make_map.py -ut $thres -d $directory -r $res

    # # MODIFY AUS
    echo " MODIFYING AUS -------------------------------------------"
    thres="0.065,0.18,0.38,0.30,0.35,0.38,0.55,0.41,0.41,0.45,0.50,0.45,9999.0"

    box="108,-40,154,-11"

    ./modify_latlon_box.py -ut $thres -d $directory -b $box -r $res

    # MODIFY TAKLAMAKAN
    echo " MODIFYING TALKAMAKAN -------------------------------------------"
    thres="0.065,0.18.5,0.18,0.30,0.35,0.38,0.45,0.41,0.41,0.45,0.50,0.45,9999.0"
    box="77.6,36,89,41.1"

    ./modify_latlon_box.py -ut ${thres} -d ${directory} -b $box -r $res

    # MODIFY CENTRAL US
#    echo " MODIFYING CENTRAL US -------------------------------------------"
    thres="0.065,0.18,0.20,0.50,0.45,0.38,0.40,0.50,0.50,0.25,0.50,0.45,9999.0"
    box="-126,25,-65,50"
    #box="77.6,36,89,41.1"
    ./modify_latlon_box.py -ut $thres -d $directory -r $res --latlon_box=$box

    # Modify Nothern Mexico for continuity
    echo " MODIFYING MX for Continuity -------------------------------------------"
    thres="0.065,0.18,0.20,0.50,0.45,0.38,0.45,0.50,0.41,0.23,0.50,0.45,9999.0"
    box="-117.95,18,-94.6,36"

    ./modify_latlon_box.py -ut $thres -d $directory -r $res --latlon_box=$box

done
