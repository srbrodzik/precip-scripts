#!/bin/csh

source /home/disk/meso-home/meso/.cshrc

set date = "`date -u --date="yesterday" +'%Y%m%d'`"

cd /home/disk/monsoon/precip/skewt
exec rsync -av $date srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/soundings
