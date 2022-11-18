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
import warnings
warnings.filterwarnings("ignore") 

if len(sys.argv) != 3:
    print('Usage: {} [fname] [outdir_base]'.format(sys.argv[0]))
    sys.exit()
else:
    fname = sys.argv[1]
    outdir_base = sys.argv[2]
    
# FOR TESTING
#fname = '/home/disk/monsoon/precip/cfradial/spol/rhi2/20220526/cfrad.20220526_003057.736_to_20220526_003324.478_SPOL_PrecipRhi2_RHI.nc'
#fname = '/home/disk/monsoon/precip/cfradial/spol_ncar/cfradial/spoldrx/rhi/20220607/cfrad.20220607_233059.754_to_20220607_233316.834_SPOL_PrecipRhi2_RHI.nc'
#fname = '/home/disk/monsoon/precip/cfradial/spol/rhi2/20220531/cfrad.20220531_080926.716_to_20220531_081135.508_SPOL_PrecipRhiUser_RHI.nc'
#outdir_base = '/home/disk/monsoon/precip/radar/spol/rhi'

# inputs
bindir = '/home/disk/monsoon/precip/bin'

# set desired angles
if 'Rhi1' in fname:
    desired_angles = [101,281]
elif 'Rhi2' in fname:
    desired_angles = [90,85,75,74,72,60,45,30,0,315,270,225,183,137]
else:
    print('Unknown rhi type . . . exiting')
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

# read input file
radar = pyart.io.read(fname)

# get azimuth angles
angles = radar.fixed_angle['data']
for index in range(0,len(angles)):
    angle = int(angles[index])

    if angle in desired_angles:
        print('angle =',angle,'is desired')

        # check to see if image already exists
        file_out = 'research.Radar_SPOL.'+datetime_str+'.rhim_6vars_'+str(angle)+'.png'
        #print('Check to see if image exists: file_out =',outdir+'/'+file_out)
        if not os.path.isfile(outdir+'/'+file_out):

            # if angle = 270, correct transition array
            if angle == 270:
                trans = radar.extract_sweeps([index]).antenna_transition["data"]
                trans[-4:]  = [1, 1, 1, 1]
                radar.extract_sweeps([index]).antenna_transition["data"] = trans
            
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
            display.plot('PHIDP_F', sweep=index, ax=ax,vmin=-180,vmax=180,
                         cmap='nipy_spectral',
                         title='', colorbar_label='PHIDP (deg)',
                         axislabels=('Distance from radar (km)', ''))
            if angle == 101:
                display.set_limits((-150,0), (0, 18), ax=ax)
            else:
                display.set_limits((0, 150), (0, 18), ax=ax)

            # save image
            #plt.show()
            plt.savefig(outdir+'/'+file_out)

            # send file to catalog
            cmd = bindir+'/SPOL_to_FC.sh '+outdir+'/'+file_out
            #print(cmd)
            os.system(cmd)

        else:
            print('NO PLOT MADE:',file_out,' already exists')
