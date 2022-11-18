#!/bin/csh

source /home/disk/meso-home/meso/.cshrc

set date = "`date -u +'%Y%m%d'`"

exec /home/disk/monsoon/precip/bin/run.skewt.cwb_edt.test.R $date 46692

