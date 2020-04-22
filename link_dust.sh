#!/bin/bash -x 

for mon in $(seq -f "%02g" 1 12); do
    for it in 1 2 3 4 5 6; do
	dir=../../../soil/tile${it}
	dir1=bsmfv3/${mon}/tile${it}
	pushd ${dir1}
	rm clay.dat
	rm sand.dat
	ln -sf $dir/clay.dat .
	ln -sf $dir/sand.dat .
	popd
    done
done

# for mon in $(seq -f "%02g" 1 12); do
#     for it in 1 2 3 4 5 6; do
#         dir=fengsha/${mon}/tile${it}
#         dir1=../fengsha_thres_map/bsmfv3/${mon}/tile${it}
#         cp -f $dir/clay.dat $dir1
#         cp -f $dir/sand.dat $dir1
#         cp -f $dir/uthr.dat $dir1/
#     done
# done
