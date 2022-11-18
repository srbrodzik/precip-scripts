#!/bin/csh

# get spol radar data

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip
setenv PROJ_DIR $DATA_DIR/git/lrose-precip/projDir

cd $DATA_DIR/bin

GetCwbData.py3 \
    --verbose \
    --platform RADAR \
    --ftpSubDir SPOKA \
    --localDirBase $DATA_DIR/cfradial/spol/ \
    --fileSuffix nc \
    --start "2022 06 06 00 00 00" \
    --end "2022 06 07 00 00 00" \
    --runOnce \
    --lookbackSecs 111600

#sortSpolFiles.py3

