#!/bin/csh

# get asd windpro data from DongSha

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip

cd $DATA_DIR/bin

GetCwbData.py3 \
    --verbose \
    --debug \
    --platform WINDPRO \
    --ftpSubDir DongSha/bufr \
    --localDirBase $DATA_DIR/raw/windpro/DongSha/bufr \
    --fileSuffix 'bufr' \
    --realtime \
    --runOnce \
    --lookbackSecs 3600

cd /home/disk/monsoon/precip/raw/windpro/DongSha
rsync -av bufr srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/windpro/DongSha

