#!/usr/bin/python3

import os
import shutil

inDir = os.environ.get('DATA_DIR')+'/cfradial/spol'
rhiDir = inDir+'/rhi'
surDir = inDir+'/sur'

for file in os.listdir(inDir):
    if file.startswith('cfradial') and file.endswith('nc'):
        (prefix,dateTime,junk,junk,junk) = file.split('.')
        (date,time) = dateTime.split('_')
        if 'RHI' in file:
            outDir = rhiDir+'/'+date
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            shutil.move(inDir+'/'+file,
                        outDir+'/'+file)
        elif 'PPI' in file:
            outDir = ppiDir+'/'+date
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            shutil.move(inDir+'/'+file,
                        outDir+'/'+file)
