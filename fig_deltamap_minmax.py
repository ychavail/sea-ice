##################################################################
# Description:
# Code name: fig_deltamap_minmax.py
# Date of creation: 2019/01/17
# Date of last modification: 2019/01/17
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import functions_plot as fct_p
import netCDF4 as netcdf
import seaborn as sns
import random
import sys
import time as tt
start_time = tt.time()

## Initialization
var         = 'tasmin'
indice      = 'qmin05'
indice_name = 'seasonal 5th percentile'
extrema     = 'mean'
units       = '[K]'
scale       = 'global'
path        = '/exec/yanncha/sea_ice/'
seasons     = ['SON','DJFM','AMJ']
subplots    = [131,132,133]
infinity	= 'both'
palette		= plt.cm.seismic
levels		= [-4,-3,-2,-1,0,1,2,3,4]
# pour mean: [-4,-3,-2,-1,0,1,2,3,4]


## Creating a mask on land
dataset     = xr.open_dataset('/klmx1/leduc/climex-core-qc/kay/195001/sftlf_kay_195001_se.nc')
lon_min     = -80.
lon_max     = -56.
lat_min     = 45.
lat_max     = 63.
dsSub       = dataset.where((dataset.lon>=lon_min)&(dataset.lon<lon_max)&(dataset.lat>=lat_min)&(dataset.lat<lat_max),drop=True)
sftlf       = np.array(dsSub['sftlf'][0,:,:])

## Figure initialization
fig1 = plt.figure(figsize=(18,6))

## Loop on seasons
for s in range(len(seasons)):

    ## Loading file
    file0       = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted0.nc'
    file1       = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted1.nc'
    nc0         = netcdf.Dataset(file0,'r')
    nc1         = netcdf.Dataset(file1,'r')
    ind0_       = nc0.variables[indice][:,:,:].data
    ind1_       = nc1.variables[indice][:,:,:].data
    land_mask	= np.zeros(ind0_.shape, dtype=bool)
    land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
    ind0_        = np.ma.array(ind0_,mask=land_mask)
    land_mask	= np.zeros(ind1_.shape, dtype=bool)
    land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
    ind1_        = np.ma.array(ind1_,mask=land_mask)
    lons        = nc1.variables['lon'][:,:]
    lats        = nc1.variables['lat'][:,:]
    if extrema == 'min':
        ind0_extr   = np.nanmin(ind0_,axis=0)
        ind1_extr   = np.nanmin(ind1_,axis=0)
    elif extrema == 'max':
        ind0_extr   = np.nanmax(ind0_,axis=0)
        ind1_extr   = np.nanmax(ind1_,axis=0)
    elif extrema == 'mean':
        ind0_extr   = np.nanmean(ind0_,axis=0)
        ind1_extr   = np.nanmean(ind1_,axis=0)

    ## Plotting
    if s == 0:
        im = fct_p.map_contourfQC(fig1,subplots[s],ind0_extr-ind1_extr,lons,lats,seasons[s],'D'+extrema+' - '+indice+' - '+var+': no ice - ice '+units,levels,infinity,palette)
    else:
        im = fct_p.map_contourfQC(fig1,subplots[s],ind0_extr-ind1_extr,lons,lats,seasons[s],'',levels,infinity,palette)

    print('### Season '+seasons[s]+' done! (%d seconds)' % (tt.time() - start_time))


fig1.subplots_adjust(right=0.8)
cbar_ax = fig1.add_axes([0.85, 0.3, 0.01, 0.4])
fig1.colorbar(im,cax=cbar_ax)
fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/fig_'+var+'_'+indice+'_'+extrema+'_deltamap.png',dpi=300)
