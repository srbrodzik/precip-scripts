#! /bin/csh

# make SPOL images

source /home/disk/meso-home/brodzik/.cshrc

setenv DATA_DIR /home/disk/monsoon/precip

cd $DATA_DIR/bin

MakeSpolImages.py3 \
    --debug \
    --verbose \
    --ncDirBase $DATA_DIR/cfradial/spol \
    --imageDirBase $DATA_DIR/radar/spol_test \
    --binDir /home/disk/monsoon/precip/bin \
    --runOnce \
    --start "2022 05 31 01 00 00" \
    --end "2022 05 31 01 30 00" \
    --lookbackSecs 3600  

