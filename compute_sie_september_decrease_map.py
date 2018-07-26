##################################################################
# Description: Compute the NH-spatial field of the global sea ice extent at its annual minimum (september) of particular runs of CanESM2-LE when sea ice extent is exceptionnally low and a few years around.
# Code name: compute_sie_september_decrease_map.py
# Date of creation: 2018/04/06
# Date of last modification: 2018/04/09
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

## historical-r2 - r3i1p1 - 2002
nc13	= netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r2/day/seaIce/sic/r3i1p1/sic_day_CanESM2_historical-r2_r3i1p1_19500101-20201231.nc','r')
time13	= nc13.variables['time']
sic13	= nc13.variables['sic'][:,32:,:]
lat	= nc13.variables['lat'][32:]
lon	= nc13.variables['lon'][:]

years13	= np.arange(2000,2006)
for y in years13:
	ind_t	= fct_t.selmonthyear(y,9,time13[:],time13.units,time13.calendar)
	sic13_y	= np.mean(sic13[ind_t[0],:,:],axis=0)
	sic13_y	= np.expand_dims(sic13_y,axis=0)
	if y == years13[0]:
		sie13	= sic13_y
	else:
		sie13	= np.concatenate((sie13,sic13_y),axis=0)


## historical-r5 - r10i1p1 - 2012
nc50	= netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r5/day/seaIce/sic/r10i1p1/sic_day_CanESM2_historical-r5_r10i1p1_19500101-20201231.nc','r')
time50	= nc50.variables['time']
sic50	= nc50.variables['sic'][:,32:,:]

years50	= np.arange(2010,2016)
for y in years50:
	ind_t	= fct_t.selmonthyear(y,9,time50[:],time50.units,time50.calendar)
	sic50_y	= np.mean(sic50[ind_t[0],:,:],axis=0)
	sic50_y	= np.expand_dims(sic50_y,axis=0)
	if y == years50[0]:
		sie50	= sic50_y
	else:
		sie50	= np.concatenate((sie50,sic50_y),axis=0)


# saving data of sea ice extent in a netcdf file
outputdir	= '/exec/yanncha/abrupt_changes/'
outputfilename 	= (outputdir+'sie_september_decrease_map_CanESM2-LE.nc')
outputfile	= netcdf.Dataset(outputfilename,'w',format='NETCDF4')
outputfile.createDimension('lat',len(lat))
outputfile.createDimension('lon',len(lon))
outputfile.createDimension('time',len(years13))
sie13_		= outputfile.createVariable('sie13','f8',('time','lat','lon',))
sie50_		= outputfile.createVariable('sie50','f8',('time','lat','lon',))
time13_  	= outputfile.createVariable('time13','i2',('time',))
time50_  	= outputfile.createVariable('time50','i2',('time',))
lat_ 		= outputfile.createVariable('lat','i2',('lat',))
lon_ 		= outputfile.createVariable('lon','i2',('lon',))
#family_ 	= outputfile.createVariable('family','str',('sim',))
#member_	= outputfile.createVariable('member','str',('sim',))
sie13_[:,:,:]	= sie13[:,:,:]
sie50_[:,:,:]	= sie50[:,:,:]
time13_[:]	= years13[:]
time50_[:]	= years50[:]
lat_[:]		= lat[:]
lon_[:]		= lon[:]
#family_[:]     = family[:]
#member_[:]     = member[:]
sie13_.units	= "%"
sie50_.units	= "%"
lat_.units	= "degree North"
lon_.units	= "degree East"
outputfile.description  = "Sea ice extent in the Northern Hemisphere in september from the CanESM2-LE."
outputfile.history      = ('Created '+tt.ctime())
outputfile.contact      = 'chavaillaz.yann@ouranos.ca'
outputfile.close()

