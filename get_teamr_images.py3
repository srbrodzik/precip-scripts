#!/usr/bin/python3

import os
import sys
import time
from datetime import timedelta
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import shutil

def listFD(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

# User inputs
debug = True
test = False

#urlBase = 'https://radar.atm.ncu.edu.tw/media/radar/TEAMR/PPI'
urlBase = 'http://140.115.35.83/TAHOPE2022/TEAMR'
targetDirBase = '/home/disk/monsoon/precip/radar/TEAM-R'
binDir = '/home/disk/monsoon/precip/bin'
tempDir = '/tmp'

category = 'research'
platform = 'Radar_TEAMR'
ppiScans = {'ZHH':{'product':'ppi_refl_05','angle':'0005'},
            'VR':{'product':'ppi_vel_05','angle':'0005'},
            'KDPR':{'product':'ppi_rrate_05','angle':'0005'}}
rhiScans29 = {'ZHH':{'product':'rhi_refl_29','angle':'0291'},
              'VR':{'product':'rhi_vel_29','angle':'0291'},
              'ZDR':{'product':'rhi_zdr_29','angle':'0291'}}   
rhiScans209 = {'ZHH':{'product':'rhi_refl_209','angle':'2091'},
               'VR':{'product':'rhi_vel_209','angle':'2091'},
               'ZDR':{'product':'rhi_zdr_209','angle':'2091'}}   
ext = 'png'

secsPerHour = 3600
lookbackSecs = 2.5 * secsPerHour

# get time at start of interval
end = time.gmtime()
endTime = datetime(end.tm_year, end.tm_mon, end.tm_mday,
              			 end.tm_hour, end.tm_min)
startTime = endTime - timedelta(seconds=lookbackSecs)
print(startTime)

# get remote files in time window for each field in ppiScans
for field in ppiScans.keys():
    print('processing ppiScans for',field)
    for fullPath in listFD(urlBase+'/PPI/'+field, ext):
        file = os.path.basename(fullPath)
        (base,ext) = os.path.splitext(file)
        (fscan,fprod,fangle,fdatetime) = base.split('_')
        ftimeObj = datetime.strptime(fdatetime,'%Y%m%d%H%M%S')
        if fangle == ppiScans[field]['angle'] and ftimeObj >= startTime:
            fdate = ftimeObj.strftime("%Y%m%d")
            ftime = ftimeObj.strftime("%H%M%S")
            targetDir = targetDirBase+'/PPI/'+fdate
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            localList = os.listdir(targetDir)
            if file not in localList:
                print('   file:',file,'not in localList -> download')
                os.chdir(targetDir)
                cmd = 'wget '+fullPath
                os.system(cmd)
                    
                fileCatalog = category+'.'+platform+'.'+fdate+ftime+'.'+ppiScans[field]['product']+'.png'
                shutil.copy(file,tempDir+'/'+fileCatalog)
                os.chdir(tempDir)
                cmd = binDir+'/TEAMR_to_FC.sh'+' '+fileCatalog
                #print(cmd)
                os.system(cmd)
                os.remove(tempDir+'/'+fileCatalog)

# get remote files in time window for each field in rhiScans29
for field in rhiScans29.keys():
    print('processing rhiScans29 for',field)
    for fullPath in listFD(urlBase+'/RHI/'+field, ext):
        file = os.path.basename(fullPath)
        (base,ext) = os.path.splitext(file)
        (fscan,fprod,fangle,fdatetime) = base.split('_')
        ftimeObj = datetime.strptime(fdatetime,'%Y%m%d%H%M%S')
        if fangle == rhiScans29[field]['angle'] and ftimeObj >= startTime:
            fdate = ftimeObj.strftime("%Y%m%d")
            ftime = ftimeObj.strftime("%H%M%S")
            targetDir = targetDirBase+'/RHI/'+fdate
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            localList = os.listdir(targetDir)
            if file not in localList:
                print('   file:',file,'not in localList -> download')
                os.chdir(targetDir)
                cmd = 'wget '+fullPath
                os.system(cmd)
                    
                fileCatalog = category+'.'+platform+'.'+fdate+ftime+'.'+rhiScans29[field]['product']+'.png'
                shutil.copy(file,tempDir+'/'+fileCatalog)
                os.chdir(tempDir)
                cmd = binDir+'/TEAMR_to_FC.sh'+' '+fileCatalog
                #print(cmd)
                os.system(cmd)
                os.remove(tempDir+'/'+fileCatalog)

# get remote files in time window for each field in rhiScans209
for field in rhiScans209.keys():
    print('processing rhiScans209 for',field)
    for fullPath in listFD(urlBase+'/RHI/'+field, ext):
        file = os.path.basename(fullPath)
        (base,ext) = os.path.splitext(file)
        (fscan,fprod,fangle,fdatetime) = base.split('_')
        ftimeObj = datetime.strptime(fdatetime,'%Y%m%d%H%M%S')
        if fangle == rhiScans209[field]['angle'] and ftimeObj >= startTime:
            fdate = ftimeObj.strftime("%Y%m%d")
            ftime = ftimeObj.strftime("%H%M%S")
            targetDir = targetDirBase+'/RHI/'+fdate
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            localList = os.listdir(targetDir)
            if file not in localList:
                print('   file:',file,'not in localList -> download')
                os.chdir(targetDir)
                cmd = 'wget '+fullPath
                os.system(cmd)
                    
                fileCatalog = category+'.'+platform+'.'+fdate+ftime+'.'+rhiScans209[field]['product']+'.png'
                shutil.copy(file,tempDir+'/'+fileCatalog)
                os.chdir(tempDir)
                cmd = binDir+'/TEAMR_to_FC.sh'+' '+fileCatalog
                #print(cmd)
                os.system(cmd)
                os.remove(tempDir+'/'+fileCatalog)



