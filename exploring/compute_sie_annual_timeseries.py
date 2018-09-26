##################################################################
# Description: Compute timeseries of the global sea ice extent in the Northern Hemisphere on annual average from the 50 members of the CanESM2-LE ensemble. 
# Code name: compute_sie_annual_timeseries.py
# Date of creation: 2018/04/09
# Date of last modification: 2018/04/10
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import netCDF4 as netcdf                # description of the meaning of data and relations fields stored in a netcdf file
import os                               # portable way of using operating system dependent functionality
import numpy as np                      # scientific computing with Python
from datetime import datetime as dt
import time as tt
import sys

import functions_time as fct_t

start_time = tt.time()

sim_family	= ['r5']
fam_member	= ['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10']
yi1		= '1950'
yf1		= '2020'
yi2		= '2021'
yf2		= '2100'

ncarea		= netcdf.Dataset('/exec/yanncha/area_data/areacella_CanESM2.nc','r')
area		= ncarea.variables['areacella'][32:,:] # only Northern Hemisphere

# loop on simulations
family		= []
member		= []
sie		= []
for f in sim_family:
	for m in fam_member:
		
		# reading sic data from CanESM2-LE files
		nc1	= netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-'+f+'/day/seaIce/sic/'+m+'i1p1/sic_day_CanESM2_historical-'+f+'_'+m+'i1p1_'+yi1+'0101-'+yf1+'1231.nc','r')
		nc2	= netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-'+f+'/day/seaIce/sic/'+m+'i1p1/sic_day_CanESM2_historical-'+f+'_'+m+'i1p1_'+yi2+'0101-'+yf2+'1231.nc','r')
			
		# concatenating on time axis and selecting september data
		time1	= nc1.variables['time']
		time2	= nc2.variables['time']
		sic1	= nc1.variables['sic'][:,32:,:]
		sic2	= nc2.variables['sic'][:,32:,:]
		years1	= np.arange(int(yi1),int(yf1)+1)
		years2	= np.arange(int(yi2),int(yf2)+1)

		sie1	= []
		for y1 in years1:
			ind_t	= fct_t.selseasyear(y1,['ANN'],time1[:],time1.units,time1.calendar)
			sic_y1 	= np.mean(sic1[ind_t,:,:],axis=0)
			sie_y1	= np.sum(sic_y1*area/100.)
			if y1 == yi1:
				sie1 = [sie_y1]
			else:
				sie1.append(sie_y1)
			print('Family ',f,', member ',m,', year ',y1)
		
		sie2	= []
		for y2 in years2:
			ind_t	= fct_t.selseasyear(y2,['ANN'],time2[:],time2.units,time2.calendar)
			sic_y2 	= np.mean(sic2[ind_t,:,:],0)
			sie_y2	= np.sum(sic_y2*area/100.)
			if y2 == yi2:
				sie2 = [sie_y2]
			else:
				sie2.append(sie_y2)
			print('Family ',f,', member ',m,', year ',y2)

		sie_fm	= np.concatenate((sie1,sie2),0)
		if (f==sim_family[0]) and (m==fam_member[0]):
			sie	= sie_fm
			family	= [f]
			member	= [m]
		else:
			sie	= np.vstack((sie,sie_fm))
			family.append(f)
			member.append(m)
		
# saving data of sea ice extent in a netcdf file
outputdir	= '/exec/yanncha/abrupt_changes/'
outputfilename	= (outputdir+'sie_annual_timeseries_CanESM2-LE_'+sim_family[0]+'.nc')
outputfile	= netcdf.Dataset(outputfilename,'w',format='NETCDF4')
outputfile.createDimension('sim',len(sim_family)*len(fam_member))
outputfile.createDimension('time',len(years1)+len(years2))
sie_		= outputfile.createVariable('sie','f8',('sim','time',))
time_		= outputfile.createVariable('time','i2',('time',))
#family_		= outputfile.createVariable('family','str',('sim',))
#member_		= outputfile.createVariable('member','str',('sim',))
sie_[:,:]	= sie[:,:]
time_[:]	= np.concatenate((years1,years2),axis=0)
#family_[:]	= family[:]
#member_[:]	= member[:]
sie_.units	= "m2"
outputfile.description	= "Sea ice extent in the Northern Hemisphere on annual average from the CanESM2-LE."
outputfile.history	= ('Created '+tt.ctime())
outputfile.contact	= 'chavaillaz.yann@ouranos.ca'
outputfile.close()
