#!/bin/bash

month=${1}

#------------------------Set these here -------------
res='C384'
#res='C96'
#base_dir=emi_C96
base_dir=bsmfv3
#----------------------------------------------------
#for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
#for month in 03; do

    echo "SETTING DEFAULT THRESHOLDS"
    thres="0.11,0.25,0.28,0.31,0.35,0.40,0.45,0.41,0.50,0.45,0.50,0.45,9999.0"
    directory=${base_dir}/${month}
    ./make_map.py -ut $thres -d $directory -r $res
    
    # # Modify Bodele 
    # echo " MODIFYING AFRICA ----------------------------------------"
    # thres="0.11,0.25,0.28,0.30,0.35,0.38,0.55,0.41,0.50,0.45,0.50,0.45,9999.0"
    # box="14.5,13.4,18.3,16.1"
    
    # ./modify_latlon_box.py -ut $thres -d $directory -b $box -r $res
    
    # # MODIFY AUS
    echo " MODIFYING AUS -------------------------------------------"
    thres="0.11,0.25,0.35,0.30,0.31,0.38,0.55,0.41,0.50,0.45,0.50,0.45,9999.0"

    box="108,-40,154,-11"

    ./modify_latlon_box.py -ut $thres -d $directory -b $box -r $res

    # MODIFY TAKLAMAKAN and Gobi
    echo " MODIFYING TALKAMAKAN -------------------------------------------"
    thres="0.11,0.25,0.24,0.30,0.30,0.25,0.45,0.41,0.50,0.45,0.50,0.45,9999.0"
    box="75.6,36,122,41.1"

    ./modify_latlon_box.py -ut ${thres} -d ${directory} -b $box -r $res --barren=True

    # Modify Middle East
    echo " MODIFYING Middle East ----------------------------------------"
    thres="0.11,0.25,0.30,0.35,0.35,0.32,0.55,0.41,0.50,0.45,0.50,0.45,9999.0"
    box="50,19.,75,45"

    ./modify_latlon_box.py -ut $thres -d $directory -b $box -r $res --barren=True

    # # modify horn of Africa
    # echo " modify horn of Africa ----------------------------------------"
    # thres="0.11,0.25,0.28,0.35,0.35,0.40,0.45,0.41,0.50,0.45,0.50,0.45,9999.0"
    # box="35,4,55,12"
    # ./modify_latlon_box.py -ut $thres -d $directory -b $box -r $res
    
    # MODIFY CENTRAL US
    echo " MODIFYING CENTRAL US -------------------------------------------"
    thres="0.11,0.25,0.24,0.50,0.45,0.38,0.40,0.50,0.50,0.25,0.50,0.45,9999.0"
    box="-126,25,-65,50"
    
    ./modify_latlon_box.py -ut $thres -d $directory -r $res --latlon_box=$box

    # Modify Nothern Mexico for continuity
    echo " MODIFYING MX for Continuity -------------------------------------------"
    thres="0.11,0.25,0.24,0.50,0.45,0.38,0.45,0.50,0.50,0.25,0.50,0.45,9999.0"
    box="-117.95,18,-94.6,36"

    ./modify_latlon_box.py -ut $thres -d $directory -r $res --latlon_box=$box

#done
