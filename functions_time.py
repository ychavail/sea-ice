#################################################################
# Description: List of functions that define operations on time axes.
# Code name: functions_time.py
# Date of creation: 2017/05/02
# Date of last modification: 2018/03/29
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import datetime
import netCDF4 as netcdf
import numpy as np

# seltimeframe: select a timeframe according to a specific CMIP5 scenario from a time axis of a netcdf file
def seltimeframe(scenario,t_coord,t_units,t_cal):
	if scenario == 'historical':
		yi	= 1860
		yf	= 2005
	elif (scenario == 'rcp45') or (scenario == 'rcp85'):
		yi	= 2005
		yf	= 2100
	elif scenario == '1pctCO2':
		yi_tmp	= t_units[11:15]        # time axis for 1pctCO2 varies from one model to another
		if yi_tmp == "1-1-":
			yi	= 1
		else:
			yi	= int(yi_tmp)
		yf	= yi + 139
	ti		= netcdf.date2num(netcdf.datetime(yi,1,1),t_units,t_cal)
	if t_cal == '360_day':
		tf	= netcdf.date2num(netcdf.datetime(yf,12,30),t_units,t_cal)
	else:
		tf	= netcdf.date2num(netcdf.datetime(yf,12,31),t_units,t_cal)
	ind_t		= np.where(np.bitwise_and(t_coord>=ti,t_coord<=tf+1))
	
	return ind_t

# selseasyear: select timesteps from a time_array 't_coord'  with units 't_units' and corresponding to a specific year 'year' and a specific seasons 'seas'
def selseasyear(year,seas,t_coord,t_units,t_cal):
	if seas==['ANN']:
		ti	= netcdf.date2num(netcdf.datetime(year,1,1),t_units,t_cal)
		if t_cal == '360_day':
			tf	= netcdf.date2num(netcdf.datetime(year,12,30),t_units,t_cal)
		else:
			tf	= netcdf.date2num(netcdf.datetime(year,12,31),t_units,t_cal)
	if seas==['DJF']:
		ti	= netcdf.date2num(netcdf.datetime(year-1,12,1),t_units,t_cal)
		if t_cal == '360_day':
			tf	= netcdf.date2num(netcdf.datetime(year,2,30),t_units,t_cal)
		else:
			tf	= netcdf.date2num(netcdf.datetime(year,2,28),t_units,t_cal)
	if seas==['MAM']:
		ti      = netcdf.date2num(netcdf.datetime(year,3,1),t_units,t_cal)
		if t_cal == '360_day':
			tf	= netcdf.date2num(netcdf.datetime(year,5,30),t_units,t_cal)
		else:
			tf	= netcdf.date2num(netcdf.datetime(year,5,31),t_units,t_cal)
	if seas==['JJA']:
		ti	= netcdf.date2num(netcdf.datetime(year,6,1),t_units,t_cal)
		if t_cal == '360_day':
			tf	= netcdf.date2num(netcdf.datetime(year,8,30),t_units,t_cal)
		else:
			tf	= netcdf.date2num(netcdf.datetime(year,8,31),t_units,t_cal)
	if seas==['SON']:
		ti      = netcdf.date2num(netcdf.datetime(year,9,1),t_units,t_cal)
		tf      = netcdf.date2num(netcdf.datetime(year,11,30),t_units,t_cal)
	ind_t   = np.where(np.bitwise_and(t_coord>=ti,t_coord<=tf+1))

	return ind_t

# selmonthyear: select timesteps from a time_array 't_coord'  with units 't_units' and corresponding to a specific year 'year' and a specific month 'month'
def selmonthyear(year,month,t_coord,t_units,t_cal):
	ti	= netcdf.date2num(netcdf.datetime(year,month,1),t_units,t_cal)
	tf	= netcdf.date2num(netcdf.datetime(year,month+1,1),t_units,t_cal)
	ind_t   = np.where(np.bitwise_and(t_coord>=ti,t_coord<=tf))
	return ind_t
