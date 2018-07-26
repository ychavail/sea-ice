##################################################################
# Description: Prepare annual sic data for machine learning operations: len(sim_family) x len(fam_member) x len(years) vectors of lat x lon size representing mean annual sic in the 60N-90N band. 
# Code name: prepare_sic_annual_forML.py
# Date of creation: 2018/05/01
# Date of last modification: 2018/05/01
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

sim_family	= ['r1','r2','r3','r4','r5']
fam_member	= ['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10']
yi1		= '1950'
yf1		= '2020'
yi2		= '2021'
yf2		= '2100'

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
		sic1	= nc1.variables['sic'][:,51:,:]
		sic2	= nc2.variables['sic'][:,51:,:]
		years1	= np.arange(int(yi1),int(yf1)+1)
		years2	= np.arange(int(yi2),int(yf2)+1)
		
		sic_fm	= np.zeros((1,np.size(sic1,1)*np.size(sic1,2)))
		for y1 in years1:
			ind_t		= fct_t.selseasyear(y1,['ANN'],time1[:],time1.units,time1.calendar)
			sic_y1 		= np.mean(sic1[ind_t[0],:,:],axis=0)
			sic_y1_resize	= np.resize(sic_y1,(1,np.size(sic_y1)))
			if y1 == yi1:
				sic_fm = sic_y1_resize
			else:
				sic_fm = np.concatenate((sic_fm,sic_y1_resize),axis=0)
			print('Family ',f,', member ',m,', year ',y1)
		
		for y2 in years2:
			ind_t		= fct_t.selseasyear(y2,['ANN'],time2[:],time2.units,time2.calendar)
			sic_y2 		= np.mean(sic2[ind_t[0],:,:],axis=0)
			sic_y2_resize	= np.resize(sic_y2,(1,np.size(sic_y1)))
			sic_fm 		= np.concatenate((sic_fm,sic_y2_resize),axis=0)
			print('Family ',f,', member ',m,', year ',y2)

		if (f==sim_family[0]) and (m==fam_member[0]):
			sic_tot	= sic_fm
		else:
			sic_tot	= np.vstack((sic_tot,sic_fm))

sys.exit()		
# saving data of sea ice extent in a netcdf file
outputdir	= '/exec/yanncha/abrupt_changes/'
outputfilename	= (outputdir+'sic_annual_forML_CanESM2-LE.nc')
outputfile	= netcdf.Dataset(outputfilename,'w',format='NETCDF4')
outputfile.createDimension('map',np.size(sic_tot,0))
outputfile.createDimension('spatial',np.size(sic_tot,1))
sic_tot_	= outputfile.createVariable('sic','f8',('map','spatial',))
sic_tot_[:,:]	= sic_tot[:,:]
sic_tot_.units	= "% of grid cell"
outputfile.description	= "Sea ice fraction in the Northern Hemisphere (60N-90N) on annual average from the CanESM2-LE."
outputfile.history	= ('Created '+tt.ctime())
outputfile.contact	= 'chavaillaz.yann@ouranos.ca'
outputfile.close()
