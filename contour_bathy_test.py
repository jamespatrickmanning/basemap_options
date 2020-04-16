# -*- coding: utf-8 -*-
"""
Adds coastwatch supplied bathymetry contours to Basemaps
@author: JiM April 2020
Specified lat/lon ranges in hardacodes along with contour interval and # of grids to interpolate
"""
import pandas as pd
import os
from scipy.interpolate import griddata
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore') # removes warnings

######Hardcodes
# the following line points to where the proj4 is located on JiM's Toshiba laptop
os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
from mpl_toolkits.basemap import Basemap
gs=25      # number of bins in the x and y direction so,  if you want more detail, make it bigger
ss=100     # subsample input data so, if you want more detail, make it smaller
cont=[-70]    # contour level
mila=40.;mala=42.;milo=-72.;malo=-69.#min & max lat and lon
#########
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
m = Basemap(projection='merc',llcrnrlat=mila,urcrnrlat=mala,llcrnrlon=milo,urcrnrlon=malo,\
            resolution='l',ax=ax)
m.drawcoastlines()
url='https://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeCrm1.csv?topo[('+str(mala)+'):1:('+str(mila)+')][('+str(milo)+'):1:('+str(malo)+')]'
print('reading in coastwatch/usgs topography')
df=pd.read_csv(url)
df=df[1:].astype('float')# removes unit row and make all float  
print('making a grid field based on this basemap ...')   
X,Y=m.makegrid(gs,gs) # where "gs" is the gridsize specified in hardcode section
X,Y=m(X,Y)
print('converting data to basemap coordinates ...')
xlo,yla=m(df['longitude'][0:-1:ss].values,df['latitude'][0:-1:ss].values)
print('gridding bathymetry ...')
zi = griddata((xlo,yla),df['topo'][0:-1:ss].values,(X,Y),method='linear')
print('contouring bathymetry ...')
m.contour(X,Y,zi,cont,zorder=4)
plt.show()
print('done.')