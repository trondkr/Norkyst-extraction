import time, calendar
from datetime import datetime,timedelta
from netCDF4 import MFDataset,Dataset
import numpy as np
import glob
import os

__author__ = 'Trond Kristiansen'
__email__ = 'trond.kristiansen@niva.no'
__created__ = datetime(2016, 12, 6)
__modified__ = datetime(2016, 12, 6)
__version__ = "1.0"
__status__ = "Development"

def writeToFile(ioInitialized,outfilename,requiredDepth,counter,ntime,myformat,temp,startYear,endYear,selectedMonth,cdf):

    if (myformat=='NETCDF4'):myzlib = True
    else:myzlib = False

    fill_value = -9.99e+33

    if ioInitialized is False:
        ioInitialized = True
        if os.path.exists(outfilename):
            os.remove(outfilename)

        f1 = Dataset(outfilename, mode='w', format=myformat)
        f1.title = "Temperature for depth %s from Norkyst model output"%(requiredDepth)
        f1.description = "Created for month %s for years %s to %s" % (selectedMonth,startYear,endYear)
        f1.history = "Created " + time.ctime(time.time())
        f1.source = "Trond Kristiansen (trond.kristiansen@niva.no)"
        f1.type = "File in %s format created using norkyst-extraction.py"%(myformat)
        f1.link = "https://github.com/trondkr/"
        f1.Conventions = "CF-1.0"

        longitude=cdf.variables["lon_rho"][:]
        latitude=cdf.variables["lat_rho"][:]
	
        # Define dimensions
        f1.createDimension('depth', 1)
        f1.createDimension('x', np.shape(longitude)[0])
        f1.createDimension('y', np.shape(longitude)[1])
        f1.createDimension('time', None)
     
        vnc = f1.createVariable('longitude', 'd', ('x', 'y',), zlib=myzlib, fill_value=fill_value)
        vnc.long_name = 'Longitude'
        vnc.units = 'degree_east'
        vnc.standard_name = 'longitude'
        vnc[:, :] = longitude

        vnc = f1.createVariable('latitude', 'd', ('x', 'y',), zlib=myzlib, fill_value=fill_value)
        vnc.long_name = 'Latitude'
        vnc.units = 'degree_north'
        vnc.standard_name = 'latitude'
        vnc[:, :] = latitude

        vnc = f1.createVariable('depth', 'd', ('depth',), zlib=myzlib, fill_value=fill_value)
        vnc.long_name = "depth"
        vnc.units = "m"
        vnc[:] = requiredDepth

    	v_time = f1.createVariable('time', 'd', ('time',), zlib=myzlib, fill_value=fill_value)
        v_time.long_name = 'seconds since 1970-01-01 00:00:00'
        v_time.units = 'seconds since 1970-01-01 00:00:00'
        v_time.field = 'time, scalar, series'
        v_time.calendar = 'standard'

        v_temp = f1.createVariable('temp', 'f', ('time', 'x', 'y',), zlib=myzlib,
                                       fill_value=fill_value)
        v_temp.long_name = "potential temperature"
        v_temp.units = "Celsius"
        v_temp.time = "time"
        v_temp.field = "temperature, scalar, series"
        v_temp.missing_value = fill_value
        f1.close()

    else:    
        # Main writing routine  - run each time
        f1 = Dataset(outfilename, mode='a', format=myformat)
        f1.variables['time'][counter] = ntime

        print "Writing timestep",counter
        f1.variables['temp'][counter, :, :] = np.squeeze(temp)
        f1.close()