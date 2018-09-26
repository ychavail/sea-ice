##################################################################
# Description: Plot maps of the NH-spatial field of the global sea ice extent at its annual minimum (september) of particular runs of CanESM2-LE when sea ice extent is exceptionnally low and a few years around.
# Code name: plot_sie_september_decrease_map.py
# Date of creation: 2018/04/09
# Date of last modification: 2018/04/09
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import netCDF4 as netcdf                # description of the meaning of data and relations fields stored in a netcdf file
import os                               # portable way of using operating system dependent functionality
import numpy as np                      # scientific computing with Python
import mpl_toolkits                             # extension of matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime as dt
import time as tt
import sys

import functions_plot as fct_pt


# defining variables to plot
nc	= netcdf.Dataset('/exec/yanncha/abrupt_changes/sie_september_decrease_map_CanESM2-LE.nc','r')
lat	= nc.variables['lat'][:]
lon	= nc.variables['lon'][:]
time13	= nc.variables['time13'][:]
sie13	= nc.variables['sie13'][:,:,:]
time50	= nc.variables['time50'][:]
sie50	= nc.variables['sie50'][:,:,:]


# plotting maps
subplt		= [231,232,233,234,235,236]
levels		= [0,10,20,30,40,50,60,70,80,90,100]
palette		= plt.cm.YlGnBu
infinity	= 'neither'

# historical-r2 - r3i1p1
fig1		= plt.figure(figsize=(7.2,5))
for i in range(len(time13)):
	im = fct_pt.map_contourfAR(fig1,subplt[i],sie13[i,:,:],lon,lat,str(time13[i]),"",levels,infinity,palette)
fig1.subplots_adjust(right=0.8)
cbar_ax = fig1.add_axes([0.85, 0.3, 0.01, 0.4])
cbar_ax.set_xlabel('[%]', rotation=0,fontsize=7)
fig1.colorbar(im,cax=cbar_ax)
fig1.suptitle('Sea ice cover [%] in september in the historical-r2 r3i1p1 simulation of CanESM2-LE', fontsize=10)
fig1.show()
fig1.savefig('/exec/yanncha/abrupt_changes/figures/sie_september_decrease_map_r2r3.eps',dpi=300)

# historical-r5 - r10i1p1
fig2		= plt.figure(figsize=(7.2,5))
for i in range(len(time50)):
	im = fct_pt.map_contourfAR(fig2,subplt[i],sie50[i,:,:],lon,lat,str(time50[i]),"",levels,infinity,palette)
cbar_ax = fig2.add_axes([0.85, 0.3, 0.01, 0.4])
fig2.subplots_adjust(right=0.8)
fig2.colorbar(im,cax=cbar_ax)
cbar_ax.set_xlabel('[%]', rotation=0,fontsize=7)
fig2.suptitle('Sea ice cover [%] in september in the historical-r5 r10i1p1 simulation of CanESM2-LE', fontsize=10)
fig2.show()
fig2.savefig('/exec/yanncha/abrupt_changes/figures/sie_september_decrease_map_r5r10.eps',dpi=300)
