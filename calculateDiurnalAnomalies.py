import time, calendar
from datetime import datetime,timedelta
from netCDF4 import Dataset
import numpy as np
import os
import IOwriteanomalies
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


__author__ = 'Trond Kristiansen'
__email__ = 'trond.kristiansen@niva.no'
__created__ = datetime(2016, 12, 9)
__modified__ = datetime(2016, 12, 9)
__version__ = "1.0"
__status__ = "Development"


"""

This script reads the output from running norkyst-extraction.py which provides a time-series of
Norkyst values at a specific depth. This script takes that time-series and calculates daily anomalies across all years and days. 
For now, only 30 days are accepted as input as we are focusing on the month of June, but this can easily be adjusted. This program had to 
be re-written to its current layout of loops to minimize the memory consumption.

"""

def calculateYearlyAnomalies(temp,day,year,x,y,times,refdate):

	arrayOne=np.empty((24,x,y))

	print "Looking for day %s and year %s"%(day,year)
	for t in xrange(len(times)):

		currentDate=refdate+timedelta(seconds=times[t])
		
		if int(currentDate.day) == int(day) and currentDate.year==year:
			arrayOne[int(currentDate.hour),:,:]=np.squeeze(temp[t,:,:])

			print "=> Found value for hour: %s day: %s in year: %s"%(currentDate.hour,currentDate.day,currentDate.year)
	
	arrayOne=np.ma.masked_where(abs(arrayOne) > 1000, arrayOne,copy=False)

	average=np.mean(arrayOne,axis=0)
	average=np.ma.masked_where(abs(average) > 1000, average,copy=False)

	print "Average over all ", np.ma.mean(arrayOne)
	arrayOne = arrayOne[0:24,:,:] - average

	print "Average anomaly over all ", np.mean(arrayOne)

	return arrayOne

def main():

	depth=4
	startYear=1995
	endYear=1996
	selectedMonth=6 # June
	myformat="NETCDF3_CLASSIC"

	infilename='norkyst_temp_%sm_years_%s-%s_month_%s.nc'%(depth,startYear,endYear,selectedMonth)
	outfilename='norkyst_tempanomalies_%sm_years_%s-%s_month_%s.nc'%(depth,startYear,endYear,selectedMonth)
	print "Opening file: %s"%(infilename)

	cdf=Dataset(infilename)
	print "Opened input file %s"%(infilename)
		
	times=cdf.variables["time"][:]
	refdate=datetime(1948,1,1,0,0,0)
	startdate=refdate+timedelta(seconds=times[0])
	enddate=refdate+timedelta(seconds=times[-1])
	print "Time found in input data covering: %s to %s"%(startdate,enddate)
	
	x=len(cdf.dimensions["x"])
	y=len(cdf.dimensions["y"])
	
	temp=cdf.variables["temp"][:]
	longitude=cdf.variables["longitude"][:]
	latitude=cdf.variables["latitude"][:]
	
 	noyears=int(enddate.year-startdate.year+1)
	years=[startdate.year+yy for yy in xrange(noyears)]

 	finalArray=np.zeros((30,24,x,y))
 	
 	for day in xrange(30):
		for yearCounter in xrange(noyears):
			finalArray[day,:,:,:]=calculateYearlyAnomalies(temp,day+1,years[yearCounter],x,y,times,refdate)

	
	#print "Dividing by observations over years to get daily average variation %s"%(counter)
	finalArray[day,:,:,:]=(finalArray[day,:,:,:]/noyears*1.0)
	finalArray=np.ma.masked_where(abs(finalArray) > 1000, finalArray,copy=False)
	print finalArray

	delivery=np.squeeze(np.mean(finalArray,0))

	IOwriteanomalies.writeToFile(outfilename,depth,myformat,delivery,longitude,latitude,startYear,endYear,selectedMonth)


if __name__ == "__main__":

	main()
