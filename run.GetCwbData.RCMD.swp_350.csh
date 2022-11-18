#!/bin/csh

# get RCMD sweep radar data

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip

cd $DATA_DIR/bin

GetCwbData.py3 \
    --verbose \
    --platform RADAR \
    --ftpSubDir RCMD/5A_RHI_TAHOPE_350.ele \
    --localDirBase $DATA_DIR/raw/radar/rcmd.swp/5A_RHI_TAHOPE_350.ele \
    --fileSuffix ele \
#    --start "2022 05 25 00 00 00" \
#    --end "2022 06 30 00 00 00" \
#    --sleepSecs 60    
    --realtime \
    --runOnce \
    --lookbackSecs 3600

cd /home/disk/monsoon/precip/raw/radar/rcmd.swp
rsync -av 5A_RHI_TAHOPE_350.ele srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/radar/rcmd.swp
