#!/bin/csh

# get asd windpro data from TORI

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip

cd $DATA_DIR/bin

GetCwbData.py3 \
    --verbose \
    --debug \
    --platform WINDPRO \
    --ftpSubDir TORI/asd \
    --localDirBase $DATA_DIR/raw/windpro/TORI/asd \
    --fileSuffix 'asd' \
    --realtime \
    --runOnce \
    --lookbackSecs 3600

cd /home/disk/monsoon/precip/raw/windpro/TORI
rsync -av asd srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/windpro/TORI

