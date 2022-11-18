#!/usr/bin/python3

# Author: Jonathan J. Helmus (jhelmus@anl.gov)
# License: BSD 3 clause
# Modified by Stacy Brodzik (srbrodzik@gmail.com)

import os
import sys
import matplotlib.pyplot as plt
from matplotlib import ticker
import pyart
import numpy as np
from datetime import datetime
import cartopy.crs as ccrs
import warnings
warnings.filterwarnings("ignore") 

#def find_nearest(array, value):
#    array = np.asarray(array)
#    idx = (np.abs(array - value)).argmin()
#    return array[idx], idx

#if len(sys.argv) != 3:
#    print('Usage: {} [fname] [outdir_base]'.format(sys.argv[0]))
#    sys.exit()
#else:
#    fname = sys.argv[1]
#    outdir_base = sys.argv[2]
    
# FOR TESTING
fname = "/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/sur/20220607/cfrad.20220607_042450.162_to_20220607_043052.364_SPOL_SUR.nc"
#fname = "/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/sur/20220715/cfrad.20220715_120050.330_to_20220715_120648.542_SPOL_SUR.nc"
#fname = "/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/sur/20220608/cfrad.20220608_012450.352_to_20220608_013052.126_SPOL_SUR.nc"
#fname = "/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/spoldrx/sur/20220601/cfrad.20220601_223319.022_to_20220601_223538.510_SPOL_PrecipSur2_SUR.nc"
#fname = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/spoldrx/sur/20220611/cfrad.20220611_200050.710_to_20220611_200652.556_SPOL_PrecipSur1_SUR.nc'
outdir_base = '/home/disk/monsoon/precip/radar/spol_test'
#outdir_base = '/home/disk/monsoon/precip/radar/spol/ppi'

# inputs
# don't need bindir for testing; can comment out
bindir = '/home/disk/monsoon/precip/bin'

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
radar.scan_type = 'sur'
els = radar.fixed_angle['data']

# get lowest elevation angle
index = 0
angle = round(els[index],1)
print('lowest angle =',angle)

# check to see if image already exists
file_out = 'research.Radar_SPOL.'+datetime_str+'.ppim_rrate_'+str(angle).replace('.','')+'.png'
if not os.path.isfile(outdir+'/'+file_out):

    # remove transition angle flags
    subset = radar.extract_sweeps([index])
    trans = subset.antenna_transition["data"]
    trans[:] = 0
    subset.antenna_transition["data"] = trans

    # create display
    # use 'subset' instead of 'radar' to define display
    # then sweep will be 0 for all plots since subset contains only one sweep
    display = pyart.graph.RadarMapDisplay(subset)
    fig = plt.figure(figsize=(12, 4.5))
    fig.tight_layout()
    fig.suptitle('SPOL Rain Rates '+start_str+' UTC PPI '+str(angle)+' deg', fontsize=18)
    lat_lines = np.arange(22,27,.5)
    lon_lines = np.arange(118, 123,1)
    
    ax = fig.add_subplot(121, projection=ccrs.PlateCarree())

    # Add grid labels to the first plot
    gl = ax.gridlines(xlocs=lon_lines, ylocs=lat_lines, draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlocator = ticker.FixedLocator(lon_lines)
    gl.ylocator = ticker.FixedLocator(lat_lines)

    display.plot_ppi_map('RATE_HYBRID', sweep=0, ax=ax, title='',
                         fig=None,
                         vmin=0,vmax=70,
                         width=400000, height=400000,
                         colorbar_label='RATE_HYBRID (mm/hr)',
                         cmap='pyart_HomeyerRainbow',
                         #cmap='pyart_Bu10',
                         #cmap='pyart_RRate11',
                         lat_lines = lat_lines,
                         lon_lines = lon_lines,
                         #axislabels=('', 'Distance from radar (km)'),
                         #embellish = True,
                         resolution = '10m')

    ax = fig.add_subplot(122, projection=ccrs.PlateCarree())
    display.plot_ppi_map('RATE_ZH', sweep=0, ax=ax, title='',
                         fig=None,
                         vmin=0,vmax=70,
                         width=400000, height=400000,
                         colorbar_label='RATE_ZH (mm/hr)',
                         #cmap='pyart_Carbone42',
                         cmap='pyart_HomeyerRainbow',
                         #cmap='pyart_RRate11',
                         #cmap='pyart_LangRainbow12',
                         lat_lines = lat_lines,
                         lon_lines = lon_lines,
                         #axislabels=('', 'Distance from radar (km)'),
                         #embellish = True,
                         resolution = '10m')

    # Add grid labels to the other plot
    gl2 = ax.gridlines(xlocs=lon_lines, ylocs=lat_lines, draw_labels=True)
    gl2.top_labels = False
    gl2.right_labels = False

    # save plot
    plt.savefig(outdir+'/'+file_out)

    # send file to catalog
    #cmd = bindir+'/SPOL_to_FC.sh '+outdir+'/'+file_out
    #os.system(cmd)

else:
    print('NO PLOT MADE:',file_out,' already exists')
