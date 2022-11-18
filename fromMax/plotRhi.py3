#!/usr/bin/python3

import pyart
import matplotlib.pyplot as plt

radar = pyart.io.read("/home/disk/monsoon/precip/cfradial/spol/20220531/cfrad.20220531_080000.424_to_20220531_080047.680_SPOL_PrecipRhi1_RHI.nc")
radar.scan_type = 'rhi'

cmap_dict = {"DBZ": "pyart_HomeyerRainbow",
             "VEL": "pyart_balance",
             "ZDR": "pyart_Carbone42",
             "RHOHV": "pyart_Carbone42",
             "KDP": "pyart_Carbone42",
             "PHIDP": "pyart_Carbone42",}
display = pyart.graph.RadarDisplay(radar)
for sweep in range(radar.nsweeps):
    for field in cmap_dict.keys():
        #display.plot(field, sweep, cmap=cmap_dict[field])
        display.plot(field, sweep,title='',
                     colorbar_label='Reflectivity (dBZ)',
                     axislabels=('Distance from radar (km)', 'Distance above radar (km)'),
                     cmap=cmap_dict[field])
        display.set_limits((-150,0), (0, 18))
        #plt.xlim(-150,0)
        #plt.ylim(0, 20)
        #plt.show()
        plt.savefig('/home/disk/monsoon/precip/radar/spol_test/test_'+field+'.png')
        plt.close()
