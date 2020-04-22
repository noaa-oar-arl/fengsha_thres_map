#!/bin/bash +x

for month in 01 02 03 04 05 06 07 08 09 10 11 12;
do
    for t in tile1 tile2 tile3 tile4 tile5 tile6; 
    do
	rm bsmfv3/${month}/${t}/uthr.dat
    done
done

for month in 01 02 03 04 05 06 07 08 09 10 11 12;
do
    echo $month
done | xargs -I {} --max-procs=12 ./fv3_thres.sh {}
