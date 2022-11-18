#!/bin/csh

# get RCMD sweep radar data

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip

cd $DATA_DIR/bin

GetCwbData.py3 \
    --verbose \
    --platform RADAR \
    --ftpSubDir RCMD/5A_PPI_TAHOPE_0-5.azi \
    --localDirBase $DATA_DIR/raw/radar/rcmd.swp/5A_PPI_TAHOPE_0-5.azi \
    --fileSuffix azi \
    --realtime \
    --runOnce \
    --lookbackSecs 3600
    
cd /home/disk/monsoon/precip/raw/radar/rcmd.swp
rsync -av 5A_PPI_TAHOPE_0-5.azi srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/radar/rcmd.swp
