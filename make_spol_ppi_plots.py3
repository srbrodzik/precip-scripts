#!/usr/bin/python3

# Author: Jonathan J. Helmus (jhelmus@anl.gov)
# License: BSD 3 clause
# Modified by Stacy Brodzik (srbrodzik@gmail.com)

import os
import sys
import matplotlib.pyplot as plt
import pyart
import numpy as np
from datetime import datetime
import cartopy.crs as ccrs
import warnings
warnings.filterwarnings("ignore") 

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx

if len(sys.argv) != 3:
    print('Usage: {} [fname] [outdir_base]'.format(sys.argv[0]))
    sys.exit()
else:
    fname = sys.argv[1]
    outdir_base = sys.argv[2]
    
# FOR TESTING
#fname = '/home/disk/monsoon/precip/cfradial/spol/sur/20220526/cfrad.20220526_002447.684_to_20220526_003047.886_SPOL_PrecipSur1_SUR.nc'
#outdir_base = '/home/disk/monsoon/precip/radar/spol'

# inputs
bindir = '/home/disk/monsoon/precip/bin'

# set desired angles
if 'Sur1' in fname or 'Sur2' in fname:
    desired_angles = [0.5,2]
else:
    print('Unknown type . . . exiting')
    exit()

# get date and time from filename
filename = os.path.basename(fname)
(prefix,start,junk,junk,junk) = filename.split('.')
start_obj = datetime. strptime(start, '%Y%m%d_%H%M%S')
start_str = start_obj.strftime('%Y/%m/%d %H:%M:%S')
datetime_str = start_obj.strftime('%Y%m%d%H%M%S')
date = start_obj.strftime('%Y%m%d')

# create outdir if necessary
outdir = outdir_base+'/'+date
if not os.path.exists(outdir):
    os.makedirs(outdir)

# read input file & get elevation angles
radar = pyart.io.read(fname)
els = radar.fixed_angle['data']

# process desired angles
for angle in desired_angles:

    # get desired elevation angle index
    (val,index) = find_nearest(els, angle)
    print('index of angle nearest',angle,'is',index)

    # check to see if image already exists
    file_out = 'research.Radar_SPOL.'+datetime_str+'.ppim_4vars_'+str(angle).replace('.','')+'.png'
    if not os.path.isfile(outdir+'/'+file_out):

        # create display
        display = pyart.graph.RadarMapDisplay(radar)
        #fig = plt.figure(figsize=(12, 9))
        fig = plt.figure(figsize=(14, 10.5))
        fig.tight_layout()
        fig.suptitle('SPOL '+start_str+' UTC PPI '+str(angle)+' deg', fontsize=20)

        ax = fig.add_subplot(221, projection=ccrs.PlateCarree())
        display.plot_ppi_map('DBZ', sweep=0, ax=ax, title='',
                             width=400000, height=400000,
                             colorbar_label='Reflectivity (dBZ)',
                             lat_lines = np.arange(22,27,.5),
                             lon_lines = np.arange(118, 123,1),
                             #axislabels=('', 'Distance from radar (km)'),
                             resolution = '10m')

        ax = fig.add_subplot(222, projection=ccrs.PlateCarree())
        display.plot_ppi_map('VEL', sweep=0, ax=ax, title='',
                             width=400000, height=400000,
                             colorbar_label='Radial Velocity (m/s)',
                             cmap='pyart_Carbone42',
                             lat_lines = np.arange(22,27,.5),
                             lon_lines = np.arange(118, 123,1),
                             #axislabels=('', ''),
                             resolution = '10m')

        ax = fig.add_subplot(223, projection=ccrs.PlateCarree())
        display.plot_ppi_map('ZDR', sweep=0, ax=ax, title='',
                             vmin=-1,vmax=4,
                             width=400000, height=400000,
                             colorbar_label='ZDR (dB)',
                             cmap='nipy_spectral',
                             lat_lines = np.arange(22,27,.5),
                             lon_lines = np.arange(118, 123,1),
                             resolution = '10m')

        ax = fig.add_subplot(224, projection=ccrs.PlateCarree())
        display.plot_ppi_map('KDP', sweep=0, ax=ax, title='', 
                             vmin=-1,vmax=4,
                             width=400000, height=400000,
                             colorbar_label='KDP (deg/km)',
                             cmap='nipy_spectral',
                             lat_lines = np.arange(22,27,.5),
                             lon_lines = np.arange(118, 123,1),
                             #axislabels=('Distance from radar (km)', ''),
                             resolution = '10m')

        # save plot
        plt.savefig(outdir+'/'+file_out)

        # send file to catalog
        cmd = bindir+'/SPOL_to_FC.sh '+outdir+'/'+file_out
        os.system(cmd)

    else:
        print('NO PLOT MADE:',file_out,' already exists')
