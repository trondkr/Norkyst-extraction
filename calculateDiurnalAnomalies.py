import time, calendar
from datetime import datetime,timedelta
from netCDF4 import Dataset
import numpy as np
import os
import IOwriteanomalies
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys
from scipy import stats
import numpy.polynomial.polynomial as poly

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

def calculateAnomalies(temp,totalDays):

	print "=> Calculating anomalies of de-trended data"
	arrayOne=np.zeros((np.shape(temp)))

	for day in xrange(0,totalDays,1):
		for hour in xrange(0,24,1):
			test=np.squeeze(temp[day,:,:,:])
	#		print "hour %s %s mean %s"%(day,hour)
	#		print np.mean(test,axis=0)
			arrayOne[day,hour,:,:]=temp[day,hour,:,:]-np.mean(test,axis=0)
			#print "arrayone", arrayOne[day,hour,:,900]
			#print "temp", temp[day,hour,:,900]

	return arrayOne

def removeTrend(tt,days):

	fit = poly.polyfit(days,tt,1)
	fit_fn = poly.polyval(days,fit)
	fit_fn=np.flipud(np.rot90(fit_fn))

	trend=tt-fit_fn

	#print np.shape(tt),np.shape(fit_fn)

	#print "tt",tt[:,200]
	#print "fit_fn",fit_fn[:,200]
	#print detrended[:,200]
	#f, axarr = plt.subplots(2, sharex=True)
	#axarr[0].plot(days,tt[:,200],'o',color='m')
	#axarr[0].plot(days,fit_fn[:,200],'o',color='r')

	#axarr[1].plot(tt-detrended[:,200],'o')
	#print "detrended",detrended

	#plt.show()
	return tt-trend
	

def extractHourlyTemperature(temp,day,year,x,y,times,refdate):

	arrayOne=np.empty((24,x,y))

	print "Looking for day %s and year %s"%(day,year)
	for t in xrange(len(times)):

		currentDate=refdate+timedelta(seconds=times[t])
		
		if int(currentDate.day) == int(day) and currentDate.year==year:
			arrayOne[int(currentDate.hour),:,:]=np.squeeze(temp[t,:,:])

			print "Trend => Found value for hour: %s day: %s in year: %s"%(currentDate.hour,currentDate.day,currentDate.year)
	
	arrayOne=np.ma.masked_where(abs(arrayOne) > 1000, arrayOne,copy=False)
	average=np.mean(arrayOne,axis=0)
	
	print "Average anomaly over all ", np.mean(arrayOne)

	return arrayOne



def main():

	depth=10
	startYear=1995
	endYear=1996
	totalDays=30
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

	finalArray=np.zeros((totalDays,24,x,y))
	trendArray=np.zeros((24,x,y))
	hours=[hh for hh in xrange(1,25,1)]
	days=[hh for hh in xrange(1,totalDays+1,1)]
	
 	for dayCounter in xrange(totalDays):
		for yearCounter in xrange(noyears):
			year=years[yearCounter]
			day=days[dayCounter]
			
 			finalArray[dayCounter,:,:,:]=finalArray[dayCounter,:,:,:] + extractHourlyTemperature(temp,day,year,x,y,times,refdate)

 	#finalArray[dayCounter,:,:,:]=(finalArray[dayCounter,:,:,:]/yearCounter*1.0)

# 	finalArray = np.ma.masked_where(abs(finalArray) > 1000, finalArray)

	
 	for hour in xrange(len(hours)):
 		for xi in xrange(x):
 			#print hour,xi,np.mean(np.squeeze(finalArray[:,hour,xi,:]))
 			detrended = removeTrend(np.squeeze(finalArray[:,hour,xi,:]),days)
 			#print detrended
 			finalArray[:,hour,xi,:] = detrended
	
	finalArray = calculateAnomalies(finalArray,totalDays)

	finalArray = np.ma.masked_where(abs(finalArray) < 1e-14, finalArray)
	print "Averaging axis = 0 for size ",np.shape(finalArray)
	# average over all days
	finalData=np.ma.mean(finalArray,axis=0)
	print np.shape(finalData)
	print "final after mean",finalData
	
	#finalData = np.ma.masked_where(abs(finalData) > 1000, finalData,copy=False)
	
	
	IOwriteanomalies.writeToFile(outfilename,depth,myformat,finalData,longitude,latitude,startYear,endYear,selectedMonth)


if __name__ == "__main__":

	main()
