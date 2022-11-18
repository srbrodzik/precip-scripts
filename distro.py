#!/usr/bin/python3

import os
import sys
import numpy as np
from datetime import datetime
import netCDF4 as nc4
import pandas as pd
import csv

inDirBase = '/home/snowband/brodzik/precip/raw/distro'
outDirBase = '/home/snowband/brodzik/precip/netcdf/distro'
tmpDir = '/tmp'
stnid = '466880'
date = '20220516'

speedBins=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,
           1.2,1.4,1.6,1.8,2.0,2.4,2.8,3.2,3.6,4.0,
           4.8,5.6,6.4,7.2,8.0,9.6,11.2,12.8,14.4,16.0,
           19.2,22.4]
numSpeedBins = len(speedBins)

diamBins=[0.125,0.250,0.375,0.500,0.625,0.750,0.875,1.000,1.125,1.250,
          1.500,1.750,2.000,2.250,2.500,3.000,3.500,4.000,4.500,5.000,
          6.000,7.000,8.000,9.000,10.00,12.00,14.00,16.00,18.00,20.00,
          23.00,26.00]
numDiamBins = len(diamBins)

inDir = inDirBase+'/'+stnid+'/'+date
outDir = outDirBase+'/'+stnid
outFile = 'distrometer_'+stnid+'.'+date+'.nc'

for file in os.listdir(inDir):

    # Get rid of <SPECTRUM> and </SPECTRUM> in input file
    cmd = "sed 's+<SPECTRUM>++' " + inDir+'/'+file+' > '+tmpDir+'/'+file+'.tmp'
    os.system(cmd)
    cmd = "sed 's+,</SPECTRUM>++' " + tmpDir+'/'+file+'.tmp > '+tmpDir+'/'+file
    os.system(cmd)

    # initialize counts array
    counts = np.zeros((numSpeedBins,numDiamBins))
    
    # Read data into dataframe and replace NaN's with 0's
    data = pd.read_csv(tmpDir+'/'+file,header=None)
    data = data.fillna(0)

    if not os.path.isdir(outDir):
        os.makedirs(outDir)
    if not os.path.isfile(outDir+'/'+outFile):

        # Create netcdf file
        nc = createDistroNcFile(outDir,outFile,numSpeedBins,numDiamBins)

    else:

        # Add new data to existing file
        
        # Get individual entries
        dateStr = data[0]       # yyyy/mm/dd
        timeStr = data[1]       # hh:mm:ss
        rrate = data[2]
        totalRain = data[3]
        wxcode_SYNOP = data[4]
        wxcode_METAR = data[5]
        wxcode_NWS = data[6]
        refl = data[7]
        vis = data[8]
        signalAmp = data[9]
        numPart = data[10]
        sensorTemp = data[11]
        current = data[12]
        voltage = data[13]
        ke = data[14]
        snowRate = data[15]
        for i in range(0,numSpeedBins):
            for j in range(0,numDiamBins):
                counts[i,j] = data[(i*numSpeedBins)+j+16]

        with nc.Dataset(ncFile_out, "a") as dst:
            #dst[refl_name_merge][:,levelDict[level],:,:] = refl
            dst[refl_name][:,levelDict[level],:,:] = refl

    # Clean up
    os.remove(tmpDir+'/'+file)
    os.remove(tmpDir+'/'+file+'.tmp'
