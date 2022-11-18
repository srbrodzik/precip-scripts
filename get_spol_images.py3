#!/usr/bin/python3

# NETWORK NOT REACHABLE

import os
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

urlBase = 'https://tsafe.cwb.gov.tw/TAHOPE_2022/tahope_data/2022/ops/Radar_SPOL'
targetDirBase = '/home/disk/monsoon/precip/radar/spol/rhi'
binDir = '/home/disk/monsoon/precip/bin'
tempDir = '/tmp'

dateStr = '20220606'
ext = 'png'

targetDir = targetDirBase+'/'+dateStr
os.chdir(targetDir)

for fullPath in listFD(urlBase+'/'+dateStr, ext):
    cmd = 'wget '+fullPath
    os.system(cmd)
