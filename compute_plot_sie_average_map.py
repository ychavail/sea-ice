##################################################################
# Description: Compute the NH-spatial field of the global sea ice extent on 20-year averages for one particular run of the CanESM2-LE. Plot 6 maps corresponding to 6 20-year periods of the simulation. 
# Code name: compute_plot_sie_average_map.py
# Date of creation: 2018/04/12
# Date of last modification: 2018/04/13
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

import functions_time as fct_t
import functions_plot as fct_pt

start_time = tt.time()

sim_family	= ['r1','r2','r3','r4','r5']
fam_member	= ['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10']
yi1		= '1950'
yf1		= '2020'
yi2		= '2021'
yf2		= '2100'

yi	= [1981,2001,2021,2041,2061,2080]
yf	= [2000,2020,2040,2060,2080,2100]

subplt		= [231,232,233,234,235,236]
levels		= [0,10,20,30,40,50,60,70,80,90,100]
palette		= plt.cm.YlGnBu
infinity	= 'neither'

for f in sim_family:
	for m in fam_member:
		# reading sic data from CanESM2-LE files
		nc1	= netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-'+f+'/day/seaIce/sic/'+m+'i1p1/sic_day_CanESM2_historical-'+f+'_'+m+'i1p1_'+yi1+'0101-'+yf1+'1231.nc','r')
		nc2	= netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-'+f+'/day/seaIce/sic/'+m+'i1p1/sic_day_CanESM2_historical-'+f+'_'+m+'i1p1_'+yi2+'0101-'+yf2+'1231.nc','r')
			
		# concatenating on time axis, selecting data for 20-year periods and plotting maps
		time1	= nc1.variables['time']
		time2	= nc2.variables['time']
		lat	= nc1.variables['lat'][32:]
		lon	= nc1.variables['lon'][:]
		sic1	= nc1.variables['sic'][:,32:,:]
		sic2	= nc2.variables['sic'][:,32:,:]
		
		fig1		= plt.figure(figsize=(7.2,5))

		for i in range(len(yi)):
			ti	= netcdf.date2num(netcdf.datetime(yi[i],1,1),time1.units,time1.calendar)
			tf	= netcdf.date2num(netcdf.datetime(yf[i],1,1),time1.units,time1.calendar)
			if i <= 1:
				ind_t	= np.where(np.bitwise_and(time1[:]>=ti,time1[:]<=tf+1))
				sie_tmp	= sic1[ind_t[0],:,:]
				sie	= np.mean(sie_tmp,0)
			else:
				ind_t	= np.where(np.bitwise_and(time2[:]>=ti,time2[:]<=tf+1))
				sie_tmp	= sic2[ind_t[0],:,:]
				sie	= np.mean(sie_tmp,0)

			im = fct_pt.map_contourfAR(fig1,subplt[i],sie,lon,lat,str(yi[i])+'-'+str(yf[i]),"",levels,infinity,palette)

		fig1.subplots_adjust(right=0.8)
		cbar_ax = fig1.add_axes([0.85, 0.3, 0.01, 0.4])
		cbar_ax.set_xlabel('[%]', rotation=0,fontsize=7)
		fig1.colorbar(im,cax=cbar_ax)
		fig1.suptitle('Sea ice cover [%] annualy average on 20-year periods in the historical-'+f+' '+m+'i1p1 simulation of CanESM2-LE', fontsize=10)
		fig1.show()
		fig1.savefig('/exec/yanncha/abrupt_changes/figures/sie_average_map_'+f+'_'+m+'.eps',dpi=300)	
		print('Figure '+f+' '+m+' done!')
