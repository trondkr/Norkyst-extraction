import time, calendar
from datetime import datetime,timedelta
from netCDF4 import MFDataset,Dataset
import numpy as np
import grid
import glob
import tools
import os
import IOwrite

__author__ = 'Trond Kristiansen'
__email__ = 'trond.kristiansen@niva.no'
__created__ = datetime(2016, 12, 6)
__modified__ = datetime(2016, 12, 6)
__version__ = "1.0"
__status__ = "Development"


def info():
    """
    This program is run by typing: python norkysr-extraction.py in the command window.

    Task:

    I think the simplest thing is, for each grid point, to aggregate daily anomalies over 
    all days (within June, for all years), and take the average at each hour (assuming you 
    get output for each hour).  Then you have 24 averages for each grid point.  Save this as a 
    netcdf variable (dimensions lat, lon, hour).  I would then also take the maximum and minimum 
    of those 24 averages at each grid point, and write these to separate netcdf variables.  
    Do this for 4m and 10m depth.

    """

def setupDataset(year):
	base="http://thredds.met.no/thredds/dodsC/fou-hi/norkyst800m/"
	base="/work/shared/imr/NorKyst-800m/NorKyst800_hindcast_1995-2005/his/%s/"%(year)
	pattern="norkyst_800m_his.nc4_*"
	print"base+pattern)",base+pattern
	#files=glob.glob(base+pattern)
	#files.sort()

	cdf=MFDataset(base+pattern)
	times=cdf.variables["ocean_time"][:]
	mask=cdf.variables["mask_rho"][:]

	refdate=datetime(1948,1,1,0,0,0)
	startdate=refdate+timedelta(seconds=times[0])
	enddate=refdate+timedelta(seconds=times[-1])
	
	print "Time found in input data covering: %s to %s"%(startdate,enddate)
	return cdf, times, mask,refdate

def extractData(cdf,ntime,z_r,mask,requiredDepth):

#	temp=(cdf.variables["temp"][:,index1]*deltaz1 + cdf.variables["temperature"][:,index2]*deltaz2)
	temp=(cdf.variables["temp"][ntime,:,:,:])
	tempAtDepth=tools.zslice(temp, z_r, mask, requiredDepth, mode='linear')
	
	return tempAtDepth

# MAIN

def main():
	# setup ---------------------------
	requiredDepth=4
	first=True

	startYear=1995
	endYear=1996
	selectedMonth=6 # June

	myformat='NETCDF3_CLASSIC'
	outfilename='norkyst_temp_%sm_years_%s-%s_month_%s.nc'%(requiredDepth,startYear,endYear,selectedMonth)

	# end setup ---------------------------
	
	ioInitialized=False
		
	for year in xrange(startYear,endYear,1):
		# start main loop
		print "Starting loop for year %s"%(year)

		# Setup the system with input data
		cdf,times,mask,refdate = setupDataset(year)

		# Calculate the 3D array for sigma levels (only once)
		if ioInitialized is False:
			z_r = grid.setupVertical(cdf)
			counter=0

			ioInitialized=IOwrite.writeToFile(ioInitialized,outfilename,requiredDepth,0,0,
					myformat,None,startYear,endYear,selectedMonth,cdf)

		for ntime in xrange(len(times)):

			currentDate=refdate+timedelta(seconds=times[ntime])
			if (currentDate.month==selectedMonth):
				print "Extracting data for %s (start:%s)"%(currentDate,time.ctime())

				# Extract the data at current time-step
				temp = extractData(cdf,ntime,z_r,mask,requiredDepth)
				print "returned", np.mean(temp)
	
				# Write the 2D data to netcdf file
				ioInitialized=IOwrite.writeToFile(ioInitialized,
					outfilename,
					requiredDepth,
					counter,
					times[ntime],
					myformat,
					temp,
					startYear,
					endYear,
					selectedMonth,
					cdf)
				print "Extract data finished (end:%s)"%(time.ctime())
				counter+=1
		cdf.close()
		print "Finished with year %s"%(year)

if __name__ == "__main__":

	main()

