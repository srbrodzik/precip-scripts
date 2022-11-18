#!/usr/bin/python3

import os
import sys
import time
from datetime import timedelta
from datetime import datetime
import shutil

########################################################################
# Get time list for the specified time interval - must be in multiples of
# 5 minutes

def getTimeList(startTime, endTime):

    startHour = startTime.hour
    startMin = startTime.minute

    if (startMin % 5) != 0:
        startMin = round(startMin/10)*10
        if startMin == 60:
            startMin = 55
        startTime = datetime(startTime.year,startTime.month,startTime.day,
                             startTime.hour,startMin)
        
    timeList = [startTime]
    nextTime = startTime+timedelta(minutes=5)
    while nextTime <= endTime:
        timeList.append(nextTime)
        nextTime = nextTime+timedelta(minutes=5)
        
    return timeList

########################################################################
# User inputs

verbose = True
test = False

urlBase = 'https://metrq.skr.u-ryukyu.ac.jp/met_rq/weather/jmarad_raw'
targetDirBase = '/home/disk/monsoon/precip/radar/Ishigaki'
binDir = '/home/disk/monsoon/precip/bin'
tempDir = '/tmp'

category = 'research'
platform = 'Radar_Ishigaki'
products = {'ref':{'product':'ppi_refl'},
            'vel':{'product':'ppi_vel'}}

secsPerHour = 3600
lookbackSecs = 3 * secsPerHour 

########################################################################
# get current time

end = time.gmtime()
endTime = datetime(end.tm_year, end.tm_mon, end.tm_mday,
              			 end.tm_hour, end.tm_min)
startTime = endTime - timedelta(seconds=lookbackSecs)

########################################################################
# get time list in interval - must be multiples of 5 minutes

timeList = getTimeList(startTime, endTime)

########################################################################
# if file not already downloaded for time, get it, rename it and send to FC

for time in timeList:

    # check to see if file has already been downloaded
    dateStr = time.strftime("%Y%m%d")
    timeStr = time.strftime("%H%M%S")
    targetDir = targetDirBase+'/'+dateStr
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
        
    file_refl = 'ppi_47920_ref_'+dateStr+'_'+timeStr+'.png'
    file_vel  = 'ppi_47920_vel_'+dateStr+'_'+timeStr+'.png'
    fileList = [file_refl,file_vel]
    
    for file in fileList:
        os.chdir(targetDir)
        if file not in os.listdir(targetDir):
            cmd = 'wget '+urlBase+'/'+dateStr+'/'+file
            try:
                os.system(cmd)
                if 'ref' in file:
                     fileCatalog = category+'.'+platform+'.'+dateStr+timeStr+'.'+products['ref']['product']+'.png'
                else:
                     fileCatalog = category+'.'+platform+'.'+dateStr+timeStr+'.'+products['vel']['product']+'.png'
                shutil.copy(file,tempDir+'/'+fileCatalog)
                os.chdir(tempDir)
                cmd = binDir+'/Ishigaki_to_FC.sh'+' '+fileCatalog
                #print(cmd)
                os.system(cmd)
                os.remove(tempDir+'/'+fileCatalog)
            except:
                if verbose:
                    print("unable to wget: ", file, file=sys.stderr)
                continue

