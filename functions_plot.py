######################################################################
# Description: Tools to plot maps and graphs in .eps.
# Code name: functions_plot.py
# Date of creation: 2017/08/16
# Date of last modification: 2018/04/09
# Contact: chavaillaz.yann@ouranos.ca
######################################################################

## Needed packages
import mpl_toolkits		# extension of matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import regionmask


# sellandtime: take a time-lat-lon 3D array (var), average the array between two given timesteps (ti,tf) and apply a mask on land
def sellandtime(var,land, ti, tf):
	
	var_tmp1			= np.nan_to_num(var)
	var_tmp2			= np.mean(var_tmp1[ti-1:tf,:,:],0)
	var_tmp2[np.where(land == 0.)]	= np.nan	# fill array with nan above ocean
	var_new				= var_tmp2
	
	return var_new

# sellatmean: take a time-lat-lon 3D array (var), select land or ocean or global grid cells and spatially average in a latitudinal band (li -> lf) to give a timeseries
def sellatmean(var,land,lat,lon,opt_lo,li,lf):
	
	nlats		= np.size(lat)
	nlons		= np.size(lon)
	lats		= np.transpose(np.tile(lat,(nlons,1)))
	lons		= np.tile(lon,(nlats,1))
	latr		= np.deg2rad(lat)
	weights 	= np.cos(latr)
	
	var_tmp		= np.nan_to_num(var)
	for i in np.arange(0,np.size(var_tmp,0)):
		var_tmp_y				= var_tmp[i,:,:]
		if opt_lo == "land":
			var_tmp_y[np.where(land == 0.)]		= np.nan	# fill array with nan above ocean
		elif opt_lo == "ocean":		
			var_tmp_y[np.where(land == 100.)]	= np.nan	# fill array with nan above land
		var_tmp_y[np.where(lats < li)]		= np.nan		# fill array with nan everywhere except in the chosen latitudinal band
		var_tmp_y[np.where(lats > lf)]		= np.nan
		var_tmp[i,:,:]				= var_tmp_y

	# spatial average weighted according to latitude array 
	var_mean_tmp	= np.nanmean(var_tmp,axis=2)
	var_mean	= np.zeros(np.size(var_mean_tmp,0))
	for i in np.arange(0,np.size(var_mean_tmp,0)):
		ind_nonan	= ~np.isnan(var_mean_tmp[i,:])
		var_mean[i]	= np.average(var_mean_tmp[i,ind_nonan],weights=weights[ind_nonan])

	return var_mean


# sellatsum: take a time-lat-lon 3D array (var), select land or ocean or global grid cells and spatially sum taking into account area of grid cells in mio of km2 in a latitudinal band (li -> lf) to give a timeseries
def sellatsum(var,land,area,lat,lon,opt_lo,li,lf):
	
	nlats		= np.size(lat)
	nlons		= np.size(lon)
	lats		= np.transpose(np.tile(lat,(nlons,1)))
	lons		= np.tile(lon,(nlats,1))
	
	var_tmp		= np.nan_to_num(var)
	for i in np.arange(0,np.size(var_tmp,0)):
		var_tmp_y				= var_tmp[i,:,:]
		if opt_lo == "land":
			var_tmp_y[np.where(land == 0.)]		= np.nan	# fill array with nan above ocean
		elif opt_lo == "ocean":		
			var_tmp_y[np.where(land == 100.)]	= np.nan	# fill array with nan above land
		var_tmp_y[np.where(lats < li)]		= np.nan		# fill array with nan everywhere except in the chosen latitudinal band
		var_tmp_y[np.where(lats > lf)]		= np.nan
		var_tmp[i,:,:]				= var_tmp_y*area

	# spatial sum 
	var_sum_tmp	= np.nansum(var_tmp,axis=2)
	var_sum		= np.nansum(var_sum_tmp,axis=1)

	return var_sum


# selsrexsum: take a time-lat-lon 3D array (var), select land or ocean or global grid cells and spatially sum taking into account area of grid cells in mio of km2 in a srex region (or aggregation of srex regions to give a timeseries
def selsrexsum(var,land,area,lat,lon,opt_lo,srex_region):
	
	mask_SREX       = regionmask.defined_regions.srex.mask(lon, lat, xarray=False)

	var_tmp		= np.nan_to_num(var)
	for i in np.arange(0,np.size(var_tmp,0)):
		var_tmp_y				= var_tmp[i,:,:]
		if opt_lo == "land":
			var_tmp_y[np.where(land == 0.)]		= np.nan	# fill array with nan above ocean
		elif opt_lo == "ocean":		
			var_tmp_y[np.where(land == 100.)]	= np.nan	# fill array with nan above land

		# fill array with nan everywhere except in the chosen srex region
		if srex_region == "ECNA":
			var_tmp_y[(mask_SREX!=4.)&(mask_SREX!=5.)] = np.nan
		elif srex_region == "NSA":
			var_tmp_y[(mask_SREX!=7.)&(mask_SREX!=8.)] = np.nan
		elif srex_region == "AUS":
			var_tmp_y[(mask_SREX!=25.)&(mask_SREX!=26.)] = np.nan
		elif srex_region == "NCA":
			var_tmp_y[(mask_SREX!=14.)&(mask_SREX!=15.)&(mask_SREX!=16.)] = np.nan
		elif srex_region == "IND":
			var_tmp_y[mask_SREX!=23.] = np.nan
		elif srex_region == "SEA":
			var_tmp_y[mask_SREX!=24.] = np.nan

		var_tmp[i,:,:]				= var_tmp_y*area

	# spatial sum 
	var_sum_tmp	= np.nansum(var_tmp,axis=2)
	var_sum		= np.nansum(var_sum_tmp,axis=1)

	return var_sum


# selcountrymean: take a time-lat-lon 3D array (var), select grid cells over a given country and spatially average taking into account area
def selcountrymean(var,area,iso3,country):
	
	var_tmp			= np.nan_to_num(var)
	for i in np.arange(0,np.size(var_tmp,0)):
		var_tmp_y			= var_tmp[i,:,:]

		# fill array with nan everywhere except in the chosen country 
		var_tmp_y[np.where(iso3!=country)]	= np.nan
		var_tmp[i,:,:]				= var_tmp_y*area/np.nansum(area[np.where(iso3==country)])

	# spatial mean
	var_mean_tmp		= np.nansum(var_tmp,axis=2)
	var_mean		= np.nansum(var_mean_tmp,axis=1)

	return var_mean


# selgdpmean: take a time-lat-lon 3D array (var), select grid cells where the GDP per capita is low, low-middle, high-middle or high according to the World Bank and spatially average taking into account area
def selgdpmean(var,area,mat_gdp,gdp_class):
	
	Nlat,Nlon				= mat_gdp.shape
	gdp_rank				= np.zeros((Nlat,Nlon))
	gdp_rank[np.where(mat_gdp<1005.)]	= 1.
	gdp_rank[np.where(mat_gdp>1005.)]	= 2.
	gdp_rank[np.where(mat_gdp>3955.)]	= 3.
	gdp_rank[np.where(mat_gdp>12235.)]	= 4.

	var_tmp					= np.nan_to_num(var)
	for i in np.arange(0,np.size(var_tmp,0)):
		var_tmp_y			= var_tmp[i,:,:]

		# fill array with nan everywhere except in countries corresponding GDP class 
		if gdp_class == "low":
			var_tmp_y[np.where(gdp_rank!=1.)]	= np.nan
			var_tmp[i,:,:]				= var_tmp_y*area/np.nansum(area[np.where(gdp_rank==1.)])
		if gdp_class == "low_middle":
			var_tmp_y[np.where(gdp_rank!=2.)]	= np.nan
			var_tmp[i,:,:]				= var_tmp_y*area/np.nansum(area[np.where(gdp_rank==2.)])
		if gdp_class == "high_middle":
			var_tmp_y[np.where(gdp_rank!=3.)]	= np.nan
			var_tmp[i,:,:]				= var_tmp_y*area/np.nansum(area[np.where(gdp_rank==3.)])
		if gdp_class == "high":
			var_tmp_y[np.where(gdp_rank!=4.)]	= np.nan
			var_tmp[i,:,:]				= var_tmp_y*area/np.nansum(area[np.where(gdp_rank==4.)])

	# spatial mean
	var_mean_tmp		= np.nansum(var_tmp,axis=2)
	var_mean		= np.nansum(var_mean_tmp,axis=1)

	return var_mean


# map_contourf: plot a map of a lat-lon 2D array according to lat and lon (1D-arrays)
def map_contourf(fig,subplt,var,lon,lat,tit,ylab,lev,ext,colormap):
	ax	= fig.add_subplot(subplt)
	nlats	= np.size(lat)
	nlons	= np.size(lon)
	lats	= np.reshape(np.transpose(np.tile(lat,(nlons,1))),nlats*nlons)
	lons	= np.reshape(np.tile(lon,(nlats,1)),nlats*nlons)
	ax.set_ylabel(ylab,fontsize=15)
	ax.set_title(tit,fontsize=15)
	map	= Basemap(projection='robin',lon_0=0,lat_0=0,resolution='c')
	map.drawcoastlines(linewidth=0.5)
	map.drawmeridians(np.arange(0,360,30))
	map.drawparallels(np.arange(-90,90,30))
	x,y	= map(lons,lats)
	im	= plt.contourf(np.reshape(x,[nlats,nlons]),np.reshape(y,[nlats,nlons]),var,levels=lev,extend=ext,cmap=colormap)
	return im 


# map_contourf_dotted: plot a map of a lat-lon 2D array according to lat and lon (1D-arrays) and put dots where the signal is significant
def map_contourf_dotted(fig,subplt,var,sgn,lon,lat,tit,ylab,lev,lev2,ext,colormap):
	ax	= fig.add_subplot(subplt)
	nlats	= np.size(lat)
	nlons	= np.size(lon)
	lats	= np.reshape(np.transpose(np.tile(lat,(nlons,1))),nlats*nlons)
	lons	= np.reshape(np.tile(lon,(nlats,1)),nlats*nlons)
	ax.set_ylabel(ylab,fontsize=15)
	ax.set_title(tit,fontsize=15)
	map	= Basemap(projection='robin',lon_0=0,lat_0=0,resolution='c')
	map.drawcoastlines(linewidth=0.5)
	map.drawmeridians(np.arange(0,360,30))
	map.drawparallels(np.arange(-90,90,30))
	x,y	= map(lons,lats)
	im	= plt.contourf(np.reshape(x,[nlats,nlons]),np.reshape(y,[nlats,nlons]),var,levels=lev,extend=ext,cmap=colormap)
	plt.contourf(np.reshape(x,[nlats,nlons]),np.reshape(y,[nlats,nlons]),sgn,levels=lev2,hatches=["","."],colors='gray',alpha=0,linewidth=1)
	return im 


# map_contourfNA: plot a map of a lat-lon 2D array according to lat and lon (1D-arrays) over North America
def map_contourfNA(fig,subplt,var,lon,lat,tit,ylab,lev,ext,colormap):
	ax	= fig.add_subplot(subplt)
	nlats	= np.size(lat)
	nlons	= np.size(lon)
	lats	= np.reshape(np.transpose(np.tile(lat,(nlons,1))),nlats*nlons)
	lons	= np.reshape(np.tile(lon,(nlats,1)),nlats*nlons)
	ax.set_ylabel(ylab,fontsize=15)
	ax.set_title(tit,fontsize=15)
	map	= Basemap(projection='stere',lon_0=-110,lat_0=48.5,llcrnrlon=-130,llcrnrlat=20,urcrnrlon=-30,urcrnrlat=55,resolution='c')
	map.drawcoastlines(linewidth=0.5)
	map.drawmeridians(np.arange(-160,-30,30))
	map.drawparallels(np.arange(25,85,15))
	x,y	= map(lons,lats)
	im	= plt.contourf(np.reshape(x,[nlats,nlons]),np.reshape(y,[nlats,nlons]),var,levels=lev,extend=ext,cmap=colormap)
	return im 


# map_contourfAR: plot a map of a lat-lon 2D array according to lat and lon (1D-arrays) over the Arctic
def map_contourfAR(fig,subplt,var,lon,lat,tit,ylab,lev,ext,colormap):
	ax	= fig.add_subplot(subplt)
	nlats	= np.size(lat)
	nlons	= np.size(lon)
	lats	= np.reshape(np.transpose(np.tile(lat,(nlons,1))),nlats*nlons)
	lons	= np.reshape(np.tile(lon,(nlats,1)),nlats*nlons)
	ax.set_ylabel(ylab,fontsize=7)
	ax.set_title(tit,fontsize=7)
	map	= Basemap(projection='npstere',boundinglat=70,lon_0=270,resolution='l')
	map.drawcoastlines(linewidth=0.5)
	map.drawmeridians(np.arange(-180,180,30))
	map.drawparallels(np.arange(50,90,10))
	x,y	= map(lons,lats)
	im	= plt.contourf(np.reshape(x,[nlats,nlons]),np.reshape(y,[nlats,nlons]),var,levels=lev,extend=ext,cmap=colormap)
	return im 
