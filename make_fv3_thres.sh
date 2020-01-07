#!/bin/bash

thres="0.065,0.18,0.28,0.30,0.35,0.45,0.45,0.42,0.42,0.45,0.50,0.45,9999.0"

directory=/gpfs/hps3/emc/naqfc/noscrub/Barry.Baker/emissions/emi_CEDS2_C384/01

./make_map.py -ut $thres -d $directory

# MODIFY AUS

thres="0.065,0.18,.35,0.30,0.35,0.45,0.55,0.42,0.42,0.45,0.50,0.45,9999.0"
box="108,-40,154,-11"

./modify_latlon_box.py -ut $thres -d $directory -b $box

# MODIFY TAKLAMAKAN

thres="0.065,0.14,.23,0.30,0.35,0.45,0.45,0.42,0.42,0.45,0.50,0.45,9999.0"
box="77.6,36,89,41.1"

./modify_latlon_box.py -ut $thres -d $directory-b $box

