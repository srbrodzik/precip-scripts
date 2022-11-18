#!/usr/bin/python3

# Author: Jonathan J. Helmus (jhelmus@anl.gov)
# License: BSD 3 clause
# Modified by Stacy Brodzik (srbrodzik@gmail.com)

# Modified version of make_spol_rhi_plots_uw.py3
# Replaces PHIDP with PID using new cfradial files
# New files don't have volume type in file name so need to check angles

import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import pyart
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore") 

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
#fname = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/rate/rhi/20220607/cfrad.20220607_235459.748_to_20220607_235716.566_SPOL_RHI.nc'
#outdir_base = '/home/disk/monsoon/precip/radar/spol_test/rhi'

# inputs
bindir = '/home/disk/monsoon/precip/bin'
mandatory_angles1 = [101., 281.]
mandatory_angles2 = [90., 85., 75., 74., 72., 60., 45., 30., 29., 0., 315., 270., 225., 183., 180., 140., 137., 135.]

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
print('outdir =',outdir)
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

# check to see if angles are mandatory_angles1 or mandatory_angles2
mandatory1 = compareArrays(angles,mandatory_angles1)
mandatory2 = compareArrays(angles,mandatory_angles2)
print('  mandatory1 =',mandatory1)
print('  mandatory2 =',mandatory2)

if mandatory1 or mandatory2:
    for index in range(0,len(angles)):
        angle = int(angles[index])
        print('angle =',angle,'is desired')

        # check to see if image already exists
        file_out = 'research.Radar_SPOL.'+datetime_str+'.rhim_6vars_'+str(angle)+'.png'
        if not os.path.isfile(outdir+'/'+file_out):

            # create display
            display = pyart.graph.RadarDisplay(radar)
            fig = plt.figure(figsize=(12, 10))
            #fig.suptitle('SPOL '+str(angle)+' deg '+start_str, fontsize=20)
            fig.suptitle('SPOL '+start_str+' UTC RHI '+str(angle)+' deg', fontsize=20)

            ax = fig.add_subplot(321)
            display.plot('DBZ_F', sweep=index, ax=ax, title='',
                         vmin=-10,vmax=65,
                         colorbar_label='Reflectivity (dBZ)',
                         cmap='pyart_HomeyerRainbow',
                         axislabels=('', 'Distance above radar (km)'))
            if angle == 101:
                display.set_limits((-150,0), (0, 18), ax=ax)
            else:
                display.set_limits((0, 150), (0, 18), ax=ax)
    
            ax = fig.add_subplot(322)
            display.plot('VEL_F', sweep=index, ax=ax,
                         title='', colorbar_label='Radial Velocity (m/s)',
                         cmap='pyart_Carbone42',
                         axislabels=('', ''))
            if angle == 101:
                display.set_limits((-150,0), (0, 18), ax=ax)
            else:
                display.set_limits((0, 150), (0, 18), ax=ax)

            ax = fig.add_subplot(323)
            display.plot('ZDR_F', sweep=index, ax=ax,vmin=-1,vmax=4,
                         cmap='nipy_spectral',
                         axislabels=('', 'Distance above radar (km)'),
                         title='', colorbar_label='ZDR (dB)')
            if angle == 101:
                display.set_limits((-150,0), (0, 18), ax=ax)
            else:
                display.set_limits((0, 150), (0, 18), ax=ax)
            
            ax = fig.add_subplot(324)
            display.plot('RHOHV_F', sweep=index, ax=ax,vmin=0,vmax=1,
                         cmap='nipy_spectral',
                         title='', colorbar_label='RHOHV',
                         axislabels=('', ''))
            if angle == 101:
                display.set_limits((-150,0), (0, 18), ax=ax)
            else:
                display.set_limits((0, 150), (0, 18), ax=ax)

            ax = fig.add_subplot(325)
            display.plot('KDP_F', sweep=index, ax=ax,vmin=-1,vmax=4,
                         cmap='nipy_spectral',
                         title='', colorbar_label='KDP (deg/km)',
                         axislabels=('Distance from radar (km)', 'Distance above radar (km)'))
            if angle == 101:
                display.set_limits((-150,0), (0, 18), ax=ax)
            else:
                display.set_limits((0, 150), (0, 18), ax=ax)

            ax = fig.add_subplot(326)
            display.plot('PID', sweep=index, ax=ax,
                         vmin=0,vmax=19,
                         cmap=pid,
                         colorbar_flag = False,
                         title='',
                         axislabels=('Distance from radar (km)', ''))
            if angle == 101:
                display.set_limits((-150,0), (0, 18), ax=ax)
            else:
                display.set_limits((0, 150), (0, 18), ax=ax)
            display.plot_colorbar(label='PID',
                                  orient='vertical',
                                  ticks=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5],
                                  ticklabs=pid_types)

            # save image
            #plt.show()
            plt.savefig(outdir+'/'+file_out)

            # send file to catalog
            cmd = bindir+'/SPOL_to_FC.sh '+outdir+'/'+file_out
            #print(cmd)
            os.system(cmd)

        else:
            print('NO PLOT MADE:',file_out,' already exists')
