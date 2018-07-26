##################################################################
# Description: Tools to make operations on netcdf files.
# Code name: functions_netcdf.py
# Date of creation: 2017/05/15
# Date of last modification: 2017/07/24
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import os
import numpy as np
import netCDF4 as netcdf
import time as tt

# write_extremeindices: write all indices related to a given extreme event for a multi-model and multi-member ensemble 
def write_extremeindices(filename,time,hist_i,hist_d,lat,lon,list_sim,integ,integ_pos,nb_events,nb_days,int_m,int_x,int_s,freq_i,dur_m,dur_x,dur_s,freq_d,int_units,dur_units,data_description):
	# remove old file if existing
	if os.path.isfile(filename):
		os.remove(filename)
	
	# file in which to store drought indicators
	outputfile	= netcdf.Dataset(filename,'w',format='NETCDF4')
	
	# create dimensions
	outputfile.createDimension('time',len(time[:]))
	outputfile.createDimension('bnds_i',np.size(freq_i,axis=1))
	outputfile.createDimension('bnds_d',np.size(freq_d,axis=1))
	outputfile.createDimension('tick_i',len(hist_i))
	outputfile.createDimension('tick_d',len(hist_d))
	outputfile.createDimension('lat',len(lat))
	outputfile.createDimension('lon',len(lon))
	outputfile.createDimension('sim',len(list_sim))
	
	# create and fill variables
	times 		= outputfile.createVariable('time', 'f8', ('time',))
	ticks_i		= outputfile.createVariable('bnds_i', 'f4', ('tick_i',))
	ticks_d		= outputfile.createVariable('bnds_d', 'f4', ('tick_d',))
	lats		= outputfile.createVariable('lat', 'f4', ('lat',))
	lons		= outputfile.createVariable('lon', 'f4', ('lon',))
	models		= outputfile.createVariable('model', 'i2', ('sim',))
	members		= outputfile.createVariable('member', 'i2', ('sim',))
	integ_		= outputfile.createVariable('integ', 'f8', ('time','lat','lon','sim'))
	integ_pos_	= outputfile.createVariable('integ_pos', 'f8', ('time','lat','lon','sim'))
	nb_events_	= outputfile.createVariable('nb_events', 'f8', ('time','lat','lon','sim'))
	nb_days_	= outputfile.createVariable('nb_days', 'f8', ('time','lat','lon','sim'))
	int_m_		= outputfile.createVariable('int_m', 'f8', ('time','lat','lon','sim'))
	int_x_		= outputfile.createVariable('int_x', 'f8', ('time','lat','lon','sim'))
	int_s_		= outputfile.createVariable('int_s', 'f8', ('time','lat','lon','sim'))
	freq_i_		= outputfile.createVariable('freq_i', 'f8', ('time','bnds_i','lat','lon','sim'))
	dur_m_		= outputfile.createVariable('dur_m', 'f8', ('time','lat','lon','sim'))
	dur_x_		= outputfile.createVariable('dur_x', 'f8', ('time','lat','lon','sim'))
	dur_s_		= outputfile.createVariable('dur_s', 'f8', ('time','lat','lon','sim'))
	freq_d_		= outputfile.createVariable('freq_d', 'f8', ('time','bnds_d','lat','lon','sim'))
	
	times[:]		= time[:]
	ticks_i[:]		= hist_i[:]
	ticks_d[:]		= hist_d[:]
	lats[:]			= lat[:]
	lons[:]			= lon[:]
	for ii in np.arange(0,len(list_sim)):
		if list_sim[ii][0] == 'BNU-ESM':
			models[ii]	= 1
		elif list_sim[ii][0] == 'CanESM2':
			models[ii]      = 2
		elif list_sim[ii][0] == 'CESM1-BCG':
			models[ii]	= 3
		elif list_sim[ii][0] == 'GFDL-ESM2G':
			models[ii]	= 4
		elif list_sim[ii][0] == 'GFDL-ESM2M':
			models[ii]	= 5
		elif list_sim[ii][0] == 'HadGEM2-ES':
			models[ii]	= 6
		elif list_sim[ii][0] == 'inmcm4':
			models[ii]	= 7
		elif list_sim[ii][0] == 'IPSL-CM5A-LR':
			models[ii]	= 8
		elif list_sim[ii][0] == 'IPSL-CM5A-MR':
			models[ii]	= 9
		elif list_sim[ii][0] == 'IPSL-CM5B-LR':
			models[ii]	= 10
		elif list_sim[ii][0] == 'MIROC-ESM':
			models[ii]	= 11
		elif list_sim[ii][0] == 'MPI-ESM-LR':
			models[ii]	= 12
		elif list_sim[ii][0] == 'MPI-ESM-MR':
			models[ii]	= 13
		elif list_sim[ii][0] == 'NorESM1-ME':
			models[ii]	= 14
		members[ii]	= int(list_sim[ii][1][1])
	integ_[:,:,:,:]		= integ[:,:,:,:]
	integ_pos_[:,:,:,:]	= integ_pos[:,:,:,:]
	nb_events_[:,:,:,:]	= nb_events[:,:,:,:]
	nb_days_[:,:,:,:]	= nb_days[:,:,:,:]
	int_m_[:,:,:,:]		= int_m[:,:,:,:]
	int_x_[:,:,:,:]		= int_x[:,:,:,:]
	int_s_[:,:,:,:]		= int_s[:,:,:,:]
	freq_i_[:,:,:,:,:]	= freq_i[:,:,:,:,:]
	dur_m_[:,:,:,:]		= dur_m[:,:,:,:]
	dur_x_[:,:,:,:]		= dur_x[:,:,:,:]
	dur_s_[:,:,:,:]		= dur_s[:,:,:,:]
	freq_d_[:,:,:,:,:]	= freq_d[:,:,:,:,:]
	
	# specificy units
	times.units		= "years since 0-1-1"
	ticks_i.units		= int_units
	ticks_d.units		= dur_units
	lats.units		= "degrees_north"
	lons.units		= "degrees_east"
	integ_.units		= int_units
	integ_pos_.units	= int_units
	nb_events_.units	= "#events"
	nb_days_.units		= "#days"
	int_m_.units		= int_units
	int_x_.units		= int_units
	int_s_.units		= int_units
	freq_i_.units		= "#events"
	dur_m_.units		= dur_units
	dur_x_.units		= dur_units
	dur_s_.units		= dur_units
	freq_d_.units		= "#events"
	
	# file description
	outputfile.description	= data_description
	outputfile.history	= ('Created '+ tt.ctime())
	outputfile.contact	= 'chavaillaz.yann@ouranos.ca'
	
	# close the nc file
	outputfile.close()
###

