##################################################################
# Description: Plot timeseries of the global sea ice extent in the Northern Hemisphere on annual average from the 50 members of the CanESM2-LE ensemble.
# Code name: plot_sie_annual_timeseries.py
# Date of creation: 2018/04/10
# Date of last modification: 2018/04/10
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import netCDF4 as netcdf                # description of the meaning of data and relations fields stored in a netcdf file
import os                               # portable way of using operating system dependent functionality
import numpy as np                      # scientific computing with Python
import matplotlib.pyplot as plt
from datetime import datetime as dt
import time as tt
import sys

# defining variables to plot
nc1	= netcdf.Dataset('/exec/yanncha/abrupt_changes/sie_annual_timeseries_CanESM2-LE_r1.nc','r')
nc2	= netcdf.Dataset('/exec/yanncha/abrupt_changes/sie_annual_timeseries_CanESM2-LE_r2.nc','r')
nc3	= netcdf.Dataset('/exec/yanncha/abrupt_changes/sie_annual_timeseries_CanESM2-LE_r3.nc','r')
nc4	= netcdf.Dataset('/exec/yanncha/abrupt_changes/sie_annual_timeseries_CanESM2-LE_r4.nc','r')
nc5	= netcdf.Dataset('/exec/yanncha/abrupt_changes/sie_annual_timeseries_CanESM2-LE_r5.nc','r')
sie1	= nc1.variables['sie'][:,:]
sie2	= nc2.variables['sie'][:,:]
sie3	= nc3.variables['sie'][:,:]
sie4	= nc4.variables['sie'][:,:]
sie5	= nc5.variables['sie'][:,:]
time	= nc1.variables['time'][:]

# plotting timeseries
fig1	= plt.figure(figsize=(7.2,5.4))
colors	= ['k','#000090','r','#8A0808','#FE9A2E','#088A08','#800080','#00CED1','#7E5835','#9E0E40']
members	= ['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i1p1','r6i1p1','r7i1p1','r8i1p1','r9i1p1','r10i1p1']

ax=fig1.add_subplot(231)
for i in range(np.size(sie1,0)):
	plt.plot(time,sie1[i,:],colors[i],linewidth=1,label=members[i])
plt.legend(bbox_to_anchor=(0.95, 0.95), loc=1, borderaxespad=0.,fontsize=7)
ax.set_title("a",fontsize=7,loc='left',fontweight='bold')
ax.set_title("historical-r1",fontsize=7)
plt.axis([1950,2100,0,4*10**15])
plt.ylabel('sea ice extent [m2]',fontsize=7)
plt.xticks([1950,1980,2010,2040,2070,2100],('','','','','',''),fontsize=7)
plt.yticks([0,10**15,2*10**15,3*10**15,4*10**15],('0','1','2','3','4e15'),fontsize=7)

ax=fig1.add_subplot(232)
for i in range(np.size(sie2,0)):
	plt.plot(time,sie2[i,:],colors[i],linewidth=1,label=members[i])
ax.set_title("b",fontsize=7,loc='left',fontweight='bold')
ax.set_title("historical-r2",fontsize=7)
plt.axis([1950,2100,0,4*10**15])
plt.xticks([1950,1980,2010,2040,2070,2100],('','','','','',''),fontsize=7)
plt.yticks([0,10**15,2*10**15,3*10**15,4*10**15],('','','','',''),fontsize=7)

ax=fig1.add_subplot(233)
for i in range(np.size(sie3,0)):
	plt.plot(time,sie3[i,:],colors[i],linewidth=1,label=members[i])
ax.set_title("c",fontsize=7,loc='left',fontweight='bold')
ax.set_title("historical-r3",fontsize=7)
plt.axis([1950,2100,0,4*10**15])
plt.xticks([1950,1980,2010,2040,2070,2100],('','','','','',''),fontsize=7)
plt.yticks([0,10**15,2*10**15,3*10**15,4*10**15],('','','','',''),fontsize=7)

ax=fig1.add_subplot(234)
for i in range(np.size(sie4,0)):
	plt.plot(time,sie4[i,:],colors[i],linewidth=1,label=members[i])
ax.set_title("d",fontsize=7,loc='left',fontweight='bold')
ax.set_title("historical-r4",fontsize=7)
plt.axis([1950,2100,0,4*10**15])
plt.ylabel('sea ice extent [m2]',fontsize=7)
plt.xticks([1950,1980,2010,2040,2070,2100],('1950','1980','2010','2040','2070','2100'),fontsize=7)
plt.yticks([0,10**15,2*10**15,3*10**15,4*10**15],('0','1','2','3','4e15'),fontsize=7)

ax=fig1.add_subplot(235)
for i in range(np.size(sie5,0)):
	plt.plot(time,sie5[i,:],colors[i],linewidth=1,label=members[i])
ax.set_title("e",fontsize=7,loc='left',fontweight='bold')
ax.set_title("historical-r5",fontsize=7)
plt.axis([1950,2100,0,4*10**15])
plt.xticks([1950,1980,2010,2040,2070,2100],('1950','1980','2010','2040','2070','2100'),fontsize=7)
plt.yticks([0,10**15,2*10**15,3*10**15,4*10**15],('','','','',''),fontsize=7)

ax=fig1.add_subplot(236)
plt.plot(time,np.mean(sie1,0),colors[0],linewidth=1,label='historical-r1')
plt.plot(time,np.mean(sie2,0),colors[1],linewidth=1,label='historical-r2')
plt.plot(time,np.mean(sie3,0),colors[2],linewidth=1,label='historical-r3')
plt.plot(time,np.mean(sie4,0),colors[3],linewidth=1,label='historical-r4')
plt.plot(time,np.mean(sie5,0),colors[4],linewidth=1,label='historical-r5')
plt.legend(bbox_to_anchor=(0.95, 0.95), loc=1, borderaxespad=0.,fontsize=7)
ax.set_title("e",fontsize=7,loc='left',fontweight='bold')
ax.set_title("multi-member mean",fontsize=7)
plt.axis([1950,2100,0,4*10**15])
plt.xticks([1950,1980,2010,2040,2070,2100],('1950','1980','2010','2040','2070','2100'),fontsize=7)
plt.yticks([0,10**15,2*10**15,3*10**15,4*10**15],('','','','',''),fontsize=7)

plt.suptitle('Northern sea ice extent on annual average according to the CanESM2-LE under the RCP8.5 scenario',fontsize=10)

fig1.show()
fig1.savefig('/exec/yanncha/abrupt_changes/figures/sie_annual_timeseries.eps',dpi=300)
