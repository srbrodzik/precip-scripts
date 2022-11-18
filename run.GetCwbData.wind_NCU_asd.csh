#!/bin/csh

# get asd windpro data from NCU

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip

cd $DATA_DIR/bin

GetCwbData_test.py3 \
    --verbose \
    --debug \
    --platform WINDPRO \
    --ftpSubDir NCU/asd \
    --localDirBase $DATA_DIR/raw/windpro/NCU/asd \
    --fileSuffix 'asd' \
    --realtime \
    --runOnce \
    --lookbackSecs 3600

cd /home/disk/monsoon/precip/raw/windpro/NCU
rsync -av asd srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/windpro/NCU

