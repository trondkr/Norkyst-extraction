
"""
This script is used to debug crash/restart files from
the new NS8km model.

Create the resulting images into an animation using:
ffmpeg -r 3 -sameq -i %03d.jpeg NS8KM_1989to1993.mp4

"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pylab import *
from netCDF4 import Dataset
import datetime

__author__   = 'Trond Kristiansen'
__email__    = 'trond.kristiansen@imr.no'
__created__  = datetime.datetime(2012, 8, 20)
__modified__ = datetime.datetime(2014, 11, 19)
__version__  = "1.0"
__status__   = "Development, 20.8.2012, 9.7.2013, 16.7.2013, 11.2.2014, 17.03.2014, 19.11.2014"

doc ="""This script reads the output of running ROMS and plots defined variables
at z-levels using pyroms. Converted to be used for KINO project 19.11.2014.
"""


def contourMap(mydata,tlon,tlat,hour,depth):
   
    plt.figure(figsize=(10,10), frameon=False)
    map = Basemap(llcrnrlon=0.0,
                  llcrnrlat=55.0,
                  urcrnrlon=48.0,
                  urcrnrlat=71.5,
                  resolution='l',projection='tmerc',lon_0=15,lat_0=66,area_thresh=200.)
          
    delta=20
    print mydata.min(),mydata.max()
    levels = np.arange(mydata.min()-0.5,mydata.max()+0.5,(mydata.max()-mydata.min())/20.)
    levels = np.arange(-0.15,0.15,0.01)
        
    x, y = map(tlon,tlat)

    map.drawcoastlines()
    map.fillcontinents(color='grey')
    map.drawcountries()
    map.drawmapboundary()

  #  map.drawmeridians(np.arange(0,360,1))
  #  map.drawparallels(np.arange(0,90,1))

   # mymaskeddata = np.ma.masked_values(mydata,mymask)
    CS1 = map.contourf(x,y,mydata,levels,cmap=cm.get_cmap('RdBu_r',len(levels)-1) )#,alpha=0.5)
    plt.colorbar(CS1,orientation='vertical',extend='both', shrink=0.5)

    plotfile='figures/'+str(depth)+'/diurnal_tempAnomalies_hour_'+str(hour+1)+'_depth_'+str(depth)+'.png'
    print "Saving plotfile: %s"%(plotfile)
    plt.savefig(plotfile, bbox_inches='tight')
    #plt.show()
    plt.close()


"""" ------------------------------------------------------------------
     MAIN
     Trond Kristiansen, 15.12.2016
     Trond.Kristiansen@niva.no
     ------------------------------------------------------------------
"""

doc="""This script reads the output from running calculateDiurnalAnomalies"""

depth=10
startYear=1995
endYear=1996
selectedMonth=6 # June

infilename='norkyst_tempanomalies_%sm_years_%s-%s_month_%s.nc'%(depth,startYear,endYear,selectedMonth)
print infilename
cdf=Dataset(infilename)

longitude=cdf.variables["longitude"][:]
latitude=cdf.variables["latitude"][:]

for hour in xrange(0,24,1):
    tempanomalies=np.squeeze(cdf.variables["tempAnomalies"][hour,:,:])
    contourMap(tempanomalies,longitude,latitude,hour,depth)

