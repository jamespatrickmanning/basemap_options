#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 06:46:41 2023
map with bathy from GEBCO
as in https://notebook.community/ueapy/ueapy.github.io/content/notebooks/2019-05-30-cartopy-map
had to change variable to "elevation"
@author: user
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import xarray as xr
import cartopy
import cartopy.crs as ccrs
bathy_file_path = Path('~/bathy/gebco_2022_n46.3184_s34.1895_w-77.168_e-59.5898.nc')# extracted from https://download.gebco.net/ 
bathy_ds = xr.open_dataset(bathy_file_path)
bathy_lon, bathy_lat, bathy_h = bathy_ds.elevation.lon, bathy_ds.elevation.lat, bathy_ds.elevation.values# had to specify "elevation" instead of "bathy"
bathy_h[bathy_h > 0] = 0 # removes land
bathy_conts = np.arange(-350, 20, 20)
coord = ccrs.PlateCarree()
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111, projection=coord)
ax.set_extent([-70.5, -67, 42.5, 45.], crs=coord);
bathy = ax.contourf(bathy_lon, bathy_lat, bathy_h, bathy_conts, transform=coord, cmap="Blues_r")
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color="k", alpha=0.5, linestyle="--")
gl.xlabels_top = False
gl.ylabels_right = False
gl.ylines = True
gl.xlines = True
fig.colorbar(bathy, ax=ax, orientation="horizontal", label="Depth (m)", shrink=0.7, pad=0.08, aspect=40);
fisher='RW' 
url='https://comet.nefsc.noaa.gov/erddap/tabledap/eMOLT.csvp?SITE%2Ctime%2Clatitude%2Clongitude%2Cdepth%2Csea_water_temperature&SITE%3E=%22'+fisher+'01%22&SITE%3C=%22'+fisher+'99%22'
df=pd.read_csv(url)
listsites=list(set(df['SITE'].values))
lats,lons=[],[]
for k in listsites:
    df1=df[df['SITE']==k]        
    lats.append(df1['latitude (degrees_north)'].values[0])
    lons.append(df1['longitude (degrees_east)'].values[0])
feature = cartopy.feature.NaturalEarthFeature(name="coastline", category="physical", scale="50m", edgecolor="0.5", facecolor="0.8")
ax.add_feature(feature)
ax.scatter(lons, lats, zorder=5, color="red", label="Wahle Lab Settlement Traps temperatures")
fig.legend(bbox_to_anchor=(0.7, 0.4))
tr2 = ccrs.Stereographic(central_latitude=43., central_longitude=-68.)
sub_ax = plt.axes([0.5, 0.4, 0.2, 0.2], projection=ccrs.Stereographic(central_latitude=43., central_longitude=-68.))
sub_ax.set_extent([-75., -65., 35., 45.])
x_co = [-70.5, -67., -67., -70.5, -70.5]
y_co = [42.5, 42.5, 45, 45, 42.5]
sub_ax.add_feature(feature)
sub_ax.plot(x_co, y_co, transform=coord, zorder=10, color="red")
ax.text( -69.75,43.5, "Curt Brown", fontsize=14)
ax.text(-68.,44.25, "Jordan Drouin", fontsize=14);