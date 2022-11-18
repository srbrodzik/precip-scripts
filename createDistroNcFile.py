import netCDF4 as nc4
import pandas as pd

def createDistroNcFile(outDir,outFile,speedBins,diamBins,data):

    numSpeedBins = len(speedBins)
    numDiamBins = len(diamBins)
    
    # Create netcdf file if one does not exist for this sensor & date
    nc = nc4.Dataset(outDir+'/'+outFile, 'w', format='NETCDF4')

    # Create dimensions
    nc.createDimension('time',None)
    nc.createDimension('speed',numSpeedBins)
    nc.createDimension('diameter',numDiamBins)

    # Create variables
    time_ID = nc.createVariable('time', 'i4', 'time')
    time_ID.units = 'time since 00:00'
    time_ID.long_name = 'times since start of day'
    speed_ID = nc.createVariable('speed', 'f4', 'speed')
    speed_ID.units = 'm/s'
    speed_ID.long_name = 'speed limits of bins'
    diameter_ID = nc.createVariable('diameter', 'f4', 'diameter')
    diameter_ID.units = 'mm'
    diameter_ID.long_name = 'diameter limits of bins'
    rrate_ID = nc.createVariable('rrate', 'f4', 'time')
    rrate_ID.units = 'mm/hr'
    rrate_ID.long_name = 'intensity of precipitation'
    totalRain_ID = nc.createVariable('totalRain', 'f4', 'time')
    totalRain_ID.units = 'mm'
    totalRain_ID.long_name = 'precipitation since reset'
    wxcode_SYNOP_ID = nc.createVariable('wxcode_SYNOP', 'a4', 'time')
    wxcode_SYNOP_ID.units = 'None'
    wxcode_SYNOP_ID.long_name = 'weather code SYNOP WaWa (Table 4080)'
    wxcode_METAR_ID = nc.createVariable('wxcode_METAR', 'a4', 'time')
    wxcode_METAR_ID.units = 'None'
    wxcode_METAR_ID.long_name = 'weather code METAR/SPECI (Table 4678)'
    wxcode_NWS_ID = nc.createVariable('wxcode_NWS', 'a4', 'time')
    wxcode_NWS_ID.units = 'None'
    wxcode_NWS_ID.long_name = 'weather code NWS'
    refl_ID = nc.createVariable('refl', 'f4', 'time')
    refl_ID.units = 'dBZ'
    refl_ID.long_name = 'radar reflectivity'
    vis_ID = nc.createVariable('vis', 'f4', 'time')
    vis_ID.units = 'm'
    vis_ID.long_name = 'MOR visibility'
    signalAmp_ID = nc.createVariable('signalAmp', 'f4', 'time')
    signalAmp_ID.units = ''
    signalAmp_ID.long_name = 'signal amplitude of laserband'
    numPart_ID = nc.createVariable('numPart', 'i4', 'time')
    numPart_ID.units = 'None'
    numPart_ID.long_name = 'number of detected particles'
    sensorTemp_ID = nc.createVariable('sensorTemp', 'f4', 'time')
    sensorTemp_ID.units = 'degC'
    sensorTemp_ID.long_name = 'temperature in sensor'
    current_ID = nc.createVariable('current', 'f4', 'time')
    current_ID.units = 'A'
    current_ID.long_name = 'heating current'
    voltage_ID = nc.createVariable('voltage', 'f4', 'time')
    voltage_ID.units = 'V'
    voltage_ID.long_name = 'sensor voltage'
    ke_ID = nc.createVariable('ke', 'f4', 'time')
    ke_ID.units = 'J/(m^2*hr)'
    ke_ID.long_name = 'kinetic energy'
    snowRate_ID = nc.createVariable('snowRate', 'f4', 'time')
    snowRate_ID.units = 'mm/hr'
    snowRate_ID = 'snow intensity'
    countsID =  nc.createVariable('counts', 'i4', ('time','speed','diameter') )
    countsID.units = 'None'
    countsID.long_name = 'particle counts in bins by size and speed'

    # Create global attributes
    nc.title = ''
    nc,source = ''
    
    # Break data into parts
    dateStr = data[0]       # yyyy/mm/dd
    timeStr = data[1]       # hh:mm:ss
    rrate = data[2]
    totalRain = data[3]
    wxcode_SYNOP = data[4]
    wxcode_METAR = data[5]
    wxcode_NWS = data[6]
    refl = data[7]
    vis = data[8]
    signalAmp = data[9]
    numPart = data[10]
    sensorTemp = data[11]
    current = data[12]
    voltage = data[13]
    ke = data[14]
    snowRate = data[15]
    for i in range(0,numSpeedBins):
        for j in range(0,numDiamBins):
            counts[i,j] = data[(i*numSpeedBins)+j+16]

    # Write data to nc file
    time_ID[:] = counts
    speed_ID[:] = speedBins
    diameter_ID[:] = diamBins
    rrate_ID[:] = rrate
    totalRain_ID[:] = totalRain
    wxcode_SYNOP_ID[:] = wxcode_SYNOP
    wxcode_METER_ID[:] = wxcode_METAR
    wxcode_METER_ID[:] = wxcode_METAR
    refl_ID[:] = refl
    vis_ID[:] = vis
    signalAmp_ID[:] = signalAmp
    numPart_ID[:] = numPart
    sensorTemp_ID[:] = sensorTemp
    current_ID[:] = current
    voltage_ID[:] = voltage
    ke_ID[:] = ke
    snowRate_ID[:] = snowRate
    counts_ID[:] = counts

    # Close netcdf file
    nc.close()
