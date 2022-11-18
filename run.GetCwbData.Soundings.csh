#!/bin/csh

# get sounding radar data

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip
setenv PROJ_DIR $DATA_DIR/git/lrose-precip/projDir

cd $DATA_DIR/bin

GetCwbData.py3 \
    --verbose \
    --platform SOUNDING \
    --localDirBase $DATA_DIR/raw/soundings \
    --fileSuffix txt \
    --realtime \
    --runOnce \
    --lookbackSecs 172800

cd /home/disk/monsoon/precip/raw/soundings
rsync -av 2022* srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/soundings

