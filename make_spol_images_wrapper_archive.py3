#!/usr/bin/python3

import os

indir_base = '/home/disk/monsoon/precip/cfradial/spol'
outdir_base = '/home/disk/monsoon/precip/radar/spol'
bindir = '/home/disk/monsoon/precip/bin'

for dir in os.listdir(indir_base):
    #if os.path.isdir(indir_base+'/'+dir) and dir.startswith('2022'):
    if dir == '20220528':
        indir = indir_base+'/'+dir
        for file in os.listdir(indir):
            print('Processing file:',file)
            if 'Rhi1' in file or 'Rhi2' in file:
                outdir = outdir_base+'/rhi'
                cmd = bindir+'/make_spol_rhi_plots.py3 '+indir+'/'+file+' '+outdir
                os.system(cmd)
            elif 'SUR' in file:
                outdir = outdir_base+'/ppi'
                cmd = bindir+'/make_spol_ppi_plots.py3 '+indir+'/'+file+' '+outdir
                os.system(cmd)
            elif 'User' in file:
                outdir = outdir_base+'/rhi'
                cmd = bindir+'/make_spol_user_plots.py3 '+indir+'/'+file+' '+outdir
                os.system(cmd)
            else:
                print('File is not ppi or rhi . . . no image generated')



