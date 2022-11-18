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
#fname = '/home/disk/monsoon/precip/cfradial/spol/rhi2/20220526/cfrad.20220526_003057.736_to_20220526_003324.478_SPOL_PrecipRhi2_RHI.nc'
#fname = '/home/disk/monsoon/precip/cfradial/spol/rhi2/20220531/cfrad.20220531_081859.984_to_20220531_082116.486_SPOL_PrecipRhi2_RHI.nc'
#fname = '/home/disk/monsoon/precip/cfradial/spol/rhi2/20220531/cfrad.20220531_080926.716_to_20220531_081135.508_SPOL_PrecipRhiUser_RHI.nc'
#outdir_base = '/home/disk/monsoon/precip/radar/spol/rhi'

# set desired angles
if 'Rhi1' in fname:
    desired_angles = [101,281]
elif 'Rhi2' in fname:
    desired_angles = [90,85,72,60,45,30,0,315,270,225,183,137]
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

# get desired elevation angle index
angles = radar.fixed_angle['data']
for index in range(0,len(angles)):
    angle = int(angles[index])

    if angle in desired_angles:
        print('angle =',angle,'is desired')

        # create display
        display = pyart.graph.RadarDisplay(radar)
        fig = plt.figure(figsize=(12, 10))
        fig.suptitle('SPOL '+str(angle)+' deg '+start_str, fontsize=20)

        ax = fig.add_subplot(221)
        display.plot('DBZ', sweep=index, ax=ax, title='Reflectivity (DBZ)',
                     colorbar_label='dBZ',
                     axislabels=('', 'North South distance from radar (km)'))
        display.set_limits((0, 200), (0, 18), ax=ax)
    
        ax = fig.add_subplot(222)
        display.plot('VEL', sweep=index, ax=ax,
                     title='Doppler Velocity (VEL)', colorbar_label='m/s',
                     cmap='pyart_Carbone42',
                     axislabels=('', ''))
        display.set_limits((0, 200), (0, 18), ax=ax)

        ax = fig.add_subplot(223)
        display.plot('ZDR', sweep=index, ax=ax,vmin=-1,vmax=4,
                     cmap='nipy_spectral',
                     title='Differential Refl (ZDR)', colorbar_label='dB')
        display.set_limits((0, 200), (0, 18), ax=ax)

        ax = fig.add_subplot(224)
        display.plot('KDP', sweep=index, ax=ax,vmin=-1,vmax=4,
                     cmap='nipy_spectral',
                     title='Specific Differential Phase (KDP)', colorbar_label='deg/km',
                     axislabels=('East West distance from radar (km)', ''))
        display.set_limits((0, 200), (0, 18), ax=ax)

        # create outfile name & save
        file_out = 'research.Radar_SPOL.'+datetime_str+'.rhim_6vars_'+str(angle)+'.png'
        #plt.show()
        plt.savefig(outdir+'/'+file_out)
