#!/usr/bin/python3

# Author: Jonathan J. Helmus (jhelmus@anl.gov)
# License: BSD 3 clause
# Modified by Stacy Brodzik (srbrodzik@gmail.com)

# NOTE: Assumes user-defined sequences contain 11 sweeps; If less than this, the script crashes; Need a more graceful exit

import os
import sys
import matplotlib as mpl
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

def compareArrays(array1,array2):
    for a in array1:
        if a in array2:
            same = True
        else:
            same = False
            break
    return same
    
# FOR TESTING
# contains user-defined angles
#fname = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/rhi/20220607/cfrad.20220607_015726.956_to_20220607_015942.198_SPOL_RHI.nc'
#fname = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/rhi/20220607/cfrad.20220607_202125.420_to_20220607_202337.338_SPOL_RHI.nc'
# contains mandatory angles
#fname = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/rhi/20220607/cfrad.20220607_235459.748_to_20220607_235716.566_SPOL_RHI.nc'  
#outdir_base = '/home/disk/monsoon/precip/radar/spol_test/rhi'

# inputs
bindir = '/home/disk/monsoon/precip/bin'
mandatory_angles = [90., 85., 75., 74., 72., 60., 45., 30., 0., 315., 270., 225., 183., 137.]

#NOTE: To create discrete colormap, try using this (choose existing cmap and number of colors desired)
#plt.imshow(I, cmap=plt.cm.get_cmap('Blues', 6))
#plt.colorbar()
#plt.clim(-1, 1)

# define color bar - copied from pid.colors in CIDD color_tables dir
colors=['#ffffff', # 0
        '#d1d0b8', # 1
        '#fed89a', # 2
        '#fe9605', # 3
        '#cd770f', # 4
        '#ff2f2f', # 5
        '#fbfb2f', # 6
        '#1fde14', # 7
        '#1fa51f', # 8
        '#0e8d0f', # 9
        '#4edfff', # 0
        '#6394f0', # 11
        '#5f54c5', # 12
        '#ffcbff', # 13
        '#f89bb7', # 14
        '#ffffff', # 15
        '#a2a180', # 16
        '#c51ea5', # 17
        '#0000cd'  # 18
]
pid = mpl.colors.LinearSegmentedColormap.from_list('pid',colors,19)
pid_types = ['None','CldDrops','Drizzle','LtRain','ModRain','HvyRain','Hail','RainHail','GrSmHail','GrRain','DrySnow','WetSnow','Ice','IrregIce','Slw','Insects','2ndTrip','Clutter','Satur']

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
num_angles = len(angles)
print('  angles =',angles)
print('  num_angles =',num_angles)

# check to see if angles are mandatory or user-defined
mandatory = compareArrays(angles,mandatory_angles)
print('  mandatory =',mandatory)

# if user-defined, continue
if not mandatory and num_angles >= 11 :

    # check to see if image already exists
    file_out = 'research.Radar_SPOL.'+datetime_str+'.rhi_user_pid.png'
    #print('Check to see if image exists: file_out =',outdir+'/'+file_out)
    if not os.path.isfile(outdir+'/'+file_out):
        
        # create display
        display = pyart.graph.RadarDisplay(radar)
        fig = plt.figure(figsize=(12, 10))
        fig.suptitle('SPOL '+start_str+' UTC User RHI Sector\n(Particle ID)', fontsize=20)
    
        ax1 = fig.add_subplot(321)
        display.plot('PID', sweep=0, ax=ax1,
                     vmin=0,vmax=19,
                     cmap=pid,
                     colorbar_flag = False,
                     title='Azimuth: '+str(int(angles[0])),
                     axislabels=('', 'Distance above radar (km)'))
        display.plot_colorbar(label='',
                              orient='vertical',
                              ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5],
                              #ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                              ticklabs=pid_types)
        display.set_limits((0, 150), (0, 18), ax=ax1)
    
        ax2 = fig.add_subplot(322)
        display.plot('PID', sweep=2, ax=ax2,
                     vmin=0,vmax=19,
                     cmap=pid,
                     colorbar_flag = False,
                     title='Azimuth: '+str(int(angles[2])),
                     axislabels=('', ''))
        display.plot_colorbar(label='',
                              orient='vertical',
                              ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5],
                              #ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                              ticklabs=pid_types)
        display.set_limits((0, 150), (0, 18), ax=ax2)
    
        ax3 = fig.add_subplot(323)
        display.plot('PID', sweep=4, ax=ax3,
                     vmin=0,vmax=19,
                     cmap=pid,
                     colorbar_flag = False,
                     title='Azimuth: '+str(int(angles[4])),
                     axislabels=('', 'Distance above radar (km)'))
        display.plot_colorbar(label='',
                              orient='vertical',
                              ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5],
                              #ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                              ticklabs=pid_types)
        display.set_limits((0, 150), (0, 18), ax=ax3)
            
        ax4 = fig.add_subplot(324)
        display.plot('PID', sweep=6, ax=ax4,
                     vmin=0,vmax=19,
                     cmap=pid,
                     colorbar_flag = False,
                     title='Azimuth: '+str(int(angles[6])),
                     axislabels=('', ''))
        display.plot_colorbar(label='',
                              orient='vertical',
                              ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5],
                              #ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                              ticklabs=pid_types)
        display.set_limits((0, 150), (0, 18), ax=ax4)

        ax5 = fig.add_subplot(325)
        display.plot('PID', sweep=8, ax=ax5,
                     vmin=0,vmax=19,
                     cmap=pid,
                     colorbar_flag = False,
                     title='Azimuth: '+str(int(angles[8])),
                     axislabels=('Distance from radar (km)', 'Distance above radar (km)'))
        display.plot_colorbar(label='',
                              orient='vertical',
                              ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5],
                              #ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                              ticklabs=pid_types)
        display.set_limits((0, 150), (0, 18), ax=ax5)

        ax6 = fig.add_subplot(326)
        display.plot('PID', sweep=10, ax=ax6,
                     vmin=0,vmax=19,
                     cmap=pid,
                     colorbar_flag = False,
                     title='Azimuth: '+str(int(angles[10])),
                     axislabels=('Distance from radar (km)', ''))
        display.plot_colorbar(label='',
                              orient='vertical',
                              ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5],
                              #ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                              ticklabs=pid_types)
        display.set_limits((0, 150), (0, 18), ax=ax6)

        ## Plot one colorbar for entire image - THIS DOESN'T WORK YET
        #fig.subplots_adjust(right=0.8)
        #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        #fig.colorbar(ax1,
        #             cax=cbar_ax,
        #             orientation='vertical')
        #             #label='Particle ID'
        #             #ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5], 
        #             #ticklabs=pid_types)

        # save image
        #plt.show()
        plt.savefig(outdir+'/'+file_out)

        # send file to catalog
        cmd = bindir+'/SPOL_to_FC.sh '+outdir+'/'+file_out
        ##print(cmd)
        os.system(cmd)

    else:
        print('NO PLOT MADE:',file_out,' already exists')
