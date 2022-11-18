#!/bin/csh

source /home/disk/meso-home/meso/.cshrc
set date = "`date -u --date="yesterday" +'%Y%m%d'`"
#exec /home/disk/monsoon/precip/bin/run.skewt.cwb_edt.R $date 46757
exec /home/disk/monsoon/precip/bin/run.skewt.cwb_edt.new.R $date 46757

