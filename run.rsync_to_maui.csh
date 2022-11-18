#!/bin.csh

source /home/disk/meso-home/meso/.cshrc

cd  /home/disk/monsoon/precip/netcdf
rsync -av himawari_ch03 srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/operational/satellite/himawari
rsync -av himawari_ch09 srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/operational/satellite/himawari
rsync -av himawari_ch10 srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/operational/satellite/himawari
rsync -av himawari_ch13 srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/operational/satellite/himawari

cd /home/disk/monsoon/precip/raw/satellite/himawari/FullDisk
rsync -av Channel03  srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/satellite/himawari/FullDisk
rsync -av Channel09  srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/satellite/himawari/FullDisk
rsync -av Channel10  srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/satellite/himawari/FullDisk
rsync -av Channel13  srbrodzik@maui.atmos.colostate.edu:/bell-scratch2/precip/DATA/raw/satellite/himawari/FullDisk



