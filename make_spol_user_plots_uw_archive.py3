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

if len(sys.argv) != 3:
    print('Usage: {} [fname] [outdir_base]'.format(sys.argv[0]))
    sys.exit()
else:
    fname = sys.argv[1]
    outdir_base = sys.argv[2]
    
# FOR TESTING
#fname = '/home/disk/monsoon/precip/cfradial/spol/20220531/cfrad.20220531_104527.028_to_20220531_104735.916_SPOL_PrecipRhiUser_RHI.nc'
#fname = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/spoldrx/rhi/20220607/cfrad.20220607_235725.152_to_20220607_235937.166_SPOL_PrecipRhiUser_RHI.nc'
#outdir_base = '/home/disk/monsoon/precip/radar/spol_test/rhi'

# inputs
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

# read input file
radar = pyart.io.read(fname)
radar.scan_type = 'rhi'

# get azimuth angles
angles = radar.fixed_angle['data']

# check to see if image already exists
file_out = 'research.Radar_SPOL.'+datetime_str+'.rhi_user.png'
#print('Check to see if image exists: file_out =',outdir+'/'+file_out)
if not os.path.isfile(outdir+'/'+file_out):
        
    # create display
    display = pyart.graph.RadarDisplay(radar)
    fig = plt.figure(figsize=(12, 10))
    fig.suptitle('SPOL '+start_str+' UTC User RHI Sector', fontsize=20)
    
    ax = fig.add_subplot(321)
    display.plot('DBZ_F', sweep=0, ax=ax,
                 vmin=-10,vmax=65,
                 cmap='pyart_HomeyerRainbow',
                 title='Azimuth: '+str(int(angles[0])),
                 colorbar_label='Reflectivity (dBZ)',
                 axislabels=('', 'Distance above radar (km)'))
    display.set_limits((0, 150), (0, 18), ax=ax)
    
    ax = fig.add_subplot(322)
    display.plot('DBZ_F', sweep=2, ax=ax,
                 vmin=-10,vmax=65,
                 cmap='pyart_HomeyerRainbow',
                 title='Azimuth: '+str(int(angles[2])),
                 colorbar_label='Reflectivity (dBZ)',
                 axislabels=('', ''))
    display.set_limits((0, 150), (0, 18), ax=ax)
    
    ax = fig.add_subplot(323)
    display.plot('DBZ_F', sweep=4, ax=ax,
                 vmin=-10,vmax=65,
                 cmap='pyart_HomeyerRainbow',
                 title='Azimuth: '+str(int(angles[4])),
                 colorbar_label='Reflectivity (dBZ)',                 
                 axislabels=('', 'Distance above radar (km)'))
    display.set_limits((0, 150), (0, 18), ax=ax)
            
    ax = fig.add_subplot(324)
    display.plot('DBZ_F', sweep=6, ax=ax,
                 vmin=-10,vmax=65,
                 cmap='pyart_HomeyerRainbow',
                 title='Azimuth: '+str(int(angles[6])),
                 colorbar_label='Reflectivity (dBZ)',                 
                 axislabels=('', ''))
    display.set_limits((0, 150), (0, 18), ax=ax)

    ax = fig.add_subplot(325)
    display.plot('DBZ_F', sweep=8, ax=ax,
                 vmin=-10,vmax=65,
                 cmap='pyart_HomeyerRainbow',
                 title='Azimuth: '+str(int(angles[8])),
                 colorbar_label='Reflectivity (dBZ)',                 
                 axislabels=('Distance from radar (km)', 'Distance above radar (km)'))
    display.set_limits((0, 150), (0, 18), ax=ax)

    ax = fig.add_subplot(326)
    display.plot('DBZ_F', sweep=10, ax=ax,
                 vmin=-10,vmax=65,
                 cmap='pyart_HomeyerRainbow',
                 title='Azimuth: '+str(int(angles[10])),
                 colorbar_label='Reflectivity (dBZ)',                 
                 axislabels=('Distance from radar (km)', ''))
    display.set_limits((0, 150), (0, 18), ax=ax)

    # save image
    #plt.show()
    plt.savefig(outdir+'/'+file_out)

    # send file to catalog
    #cmd = bindir+'/SPOL_to_FC.sh '+outdir+'/'+file_out
    ##print(cmd)
    #os.system(cmd)

else:
    print('NO PLOT MADE:',file_out,' already exists')
