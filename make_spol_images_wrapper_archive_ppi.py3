#!/usr/bin/python3

import os
from datetime import datetime, timedelta
import time

indir_base = '/home/disk/monsoon/precip/cfradial/spol'
outdir_base = '/home/disk/monsoon/precip/radar/spol'
bindir = '/home/disk/monsoon/precip/bin'

lookBackSecs = 1800

# get start and end times
#nowTime = time.gmtime()
#end = datetime(nowTime.tm_year, nowTime.tm_mon, nowTime.tm_mday,
#               nowTime.tm_hour, nowTime.tm_min, nowTime.tm_sec)
#start = end - timedelta(seconds=lookBackSecs)
start = datetime(2022,5,26,0,0,0)
end = datetime(2022,6,4,0,0,0)
endDateStr = end.strftime("%Y%m%d")
startDateStr = start.strftime("%Y%m%d")

# get dates in time interval
dates = [startDateStr]
next = start + timedelta(hours=24)
nextDateStr = next.strftime("%Y%m%d")
while nextDateStr <= endDateStr:
    dates.append(nextDateStr)
    next = next + timedelta(hours=24)
    nextDateStr = next.strftime("%Y%m%d")

# process data in time interval
for dir in os.listdir(indir_base):
    if os.path.isdir(indir_base+'/'+dir) and dir.startswith('2022'):
        if dir in dates:
            indir = indir_base+'/'+dir
            for file in os.listdir(indir):
                (junk,cfTimeStr,junk,junk,junk) = file.split('.')
                cfTime = datetime.strptime(cfTimeStr,'%Y%m%d_%H%M%S')
                if cfTime >= start and cfTime <= end:
                    print('Processing file:',file)
                    if 'Sur1' in file or 'Sur2' in file:
                        outdir = outdir_base+'/ppi'
                        cmd = bindir+'/make_spol_ppi_plots.py3 '+indir+'/'+file+' '+outdir
                        os.system(cmd)
                    else:
                        print('File is not of interest . . . no image generated')



