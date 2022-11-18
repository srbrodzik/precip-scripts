#!/usr/bin/python3

# Imports and functions
import os
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt

# explicit function to normalize array
def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)    
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

# User inputs
indir = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/sur'
nbins = 30
rng = [0,300]

# create rrate max arrays
countsHybrid = np.zeros(nbins, dtype = int)
countsPid = np.zeros(nbins, dtype = int)

for idate in os.listdir(indir):
    if idate.startswith('20220607') and os.path.isdir(indir+'/'+idate):
        for fname in os.listdir(indir+'/'+idate):
            if fname.endswith('nc'):

                print(fname)

                # open and read RATE_HYBRID and RATE_PID from input file
                ncid = nc4.Dataset(indir+'/'+idate+'/'+fname,'r')
                hybrid = np.array(ncid.variables['RATE_HYBRID'])
                pid = np.array(ncid.variables['RATE_PID'])
                ncid.close()

                hist_hybrid = np.histogram(hybrid, bins=nbins, range=rng)
                hist_pid = np.histogram(pid, bins=nbins, range=rng)

                countsHybrid = countsHybrid + hist_hybrid[0]
                countsPid = countsPid + hist_pid[0]

# normalize counts arrays
#countsHybridNorm = normalize(countsHybrid,rng[0],rng[1])
#countsPidNorm = normalize(countsPid,rng[0],rng[1])
#print('countsHybridNorm =',countsHybridNorm)
#print('countsPidNorm =',countsPidNorm)

# plot histograms
print('countsHybrid =',countsHybrid)
print('countsPid =',countsPid)

fig,ax = plt.subplots(figsize =(10,7))
ax.hist(countsHybrid,np.arange(0,310,10))
plt.show()

