#!/bin/csh

# get bufr windpro data from NCU

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip

cd $DATA_DIR/bin

GetCwbData.py3 \
    --verbose \
    --debug \
    --platform WINDPRO \
    --ftpSubDir NCU/bufr \
    --localDirBase $DATA_DIR/raw/windpro/NCU/bufr \
    --fileSuffix 'bufr' \
    --realtime \
    --runOnce \
    --lookbackSecs 3600

cd /home/disk/monsoon/precip/raw/windpro/NCU
rsync -av bufr srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/windpro/NCU

