##################################################################
# Description:
# Code name: statistics_tasmax.py
# Date of creation: 2018/10/31
# Date of last modification: 2018/11/02
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import netCDF4 as netcdf
import seaborn as sns
import functions_plot as fct_p
import random
import sys
import time as tt
start_time = tt.time()

# Initialization
path        = '/exec/yanncha/sea_ice/tasmax/tasmax_'
indice      = 'qmax95'
indice_name = '95th percentile of tasmax'
season = 'JJAS'

# Creating a mask on land
dataset     = xr.open_dataset('/klmx1/leduc/climex-core-qc/kay/195001/sftlf_kay_195001_se.nc')
lon_min     = -80.
lon_max     = -56.
lat_min     = 45.
lat_max     = 63.
dsSub       = dataset.where((dataset.lon>=lon_min)&(dataset.lon<lon_max)&(dataset.lat>=lat_min)&(dataset.lat<lat_max),drop=True)
sftlf       = np.array(dsSub['sftlf'][0,:,:])

# Loading files
file0       = path+indice+'_sorted0.nc'
nc0         = netcdf.Dataset(file0,'r')
ind0_       = nc0.variables[indice][:,:,:].data
land_mask	= np.zeros(ind0_.shape, dtype=bool)
land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
ind0_       = np.ma.array(ind0_,mask=land_mask)
ind0        = ind0_[~np.isnan(ind0_)]
file1       = path+indice+'_sorted1.nc'
nc1         = netcdf.Dataset(file1,'r')
ind1_       = nc1.variables[indice][:,:,:].data
land_mask	= np.zeros(ind1_.shape, dtype=bool)
land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
ind1_       = np.ma.array(ind1_,mask=land_mask)
ind1        = ind1_[~np.isnan(ind1_)]
file2       = path+indice+'_sorted2.nc'
nc2         = netcdf.Dataset(file2,'r')
ind2_       = nc2.variables[indice][:,:,:].data
land_mask	= np.zeros(ind2_.shape, dtype=bool)
land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
ind2_       = np.ma.array(ind2_,mask=land_mask)
ind2        = ind2_[~np.isnan(ind2_)]
lons        = nc2.variables['lon'][:,:]
lats        = nc2.variables['lat'][:,:]
del file0,nc0,file1,nc1,file2,nc2
file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/statistics_tasmax.txt','a')
file_txt.write(('### Loading files done! (%d seconds)' % (tt.time() - start_time)))
file_txt.close()

# Quantile-quantile plot
percs   = np.array([0.1,1,2,3,4,5,10,20,30,40,50,60,70,80,90,95,96,97,98,99,99.9])
qn0     = np.percentile(ind0, percs)
qn1     = np.percentile(ind1, percs)
#qn2     = np.percentile(ind2, percs)
fig1 = plt.figure(figsize=(7.2,5.1))
plt.plot(qn0,qn1,ls='',marker='o',color='#9E9E9E')
x = np.linspace(np.min((qn0.min(),qn1.min())), np.max((qn0.max(),qn1.max())))
plt.plot(x,x, color='k', ls='--')
plt.title(('Quantile-quantile plot of '+indice_name+' over Quebec'))
plt.xlabel(indice_name+' with ice [K]')
plt.ylabel(indice_name+' without ice [K]')
plt.axis([0,25,0,25])
fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/tasmax_'+indice+'_'+season+'_global_qqplot.png',dpi=300)
file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/statistics_tasmax.txt','a')
file_txt.write(('### Figure 1 done! (%d seconds)' % (tt.time() - start_time)))
file_txt.close()


# Différence entre maximum de chaque distribution en représentation spatiale
ind0_max    = np.nanmax(ind0_,axis=0)
ind1_max    = np.nanmax(ind1_,axis=0)
ind2_max    = np.nanmax(ind2_,axis=0)
fig2 = plt.figure(figsize=(7.2,5.1))
levels		= [-8,-6,-4,-2,0,2,4,6,8]
infinity	= 'both'
palette		= plt.cm.seismic
im = fct_p.map_contourfQC(fig2,111,ind0_max-ind1_max,lons,lats,('Dmax('+indice+'): no ice - ice [K]'),"",levels,infinity,palette)
fig2.subplots_adjust(right=0.8)
cbar_ax = fig2.add_axes([0.85, 0.3, 0.01, 0.4])
fig2.colorbar(im,cax=cbar_ax)
fig2.show()
fig2.savefig('/exec/yanncha/sea_ice/figures/tasmax_'+indice+'_'+season+'_diffmax_map.png',dpi=300)
file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/statistics_tasmax.txt','a')
file_txt.write(('### Figure 2 done! (%d seconds)' % (tt.time() - start_time)))
file_txt.close()


# Global distribution
fig3 = plt.figure(figsize=(7.2,5.1))
sns.distplot(random.sample(list(ind0.data), 20000),rug=True,hist=False,rug_kws={"color": '#000090'},kde_kws={"color": '#000090', "label": "no ice"})
sns.distplot(random.sample(list(ind1.data), 20000),rug=True,hist=False,rug_kws={"color": 'r'},kde_kws={"color": 'r', "label": "ice"})
sns.distplot(random.sample(list(ind2.data), 20000),rug=True,hist=False,rug_kws={"color": '#8A0808'},kde_kws={"color": '#8A0808', "label": "unclear"},axlabel='T [K]')
plt.title(('Global distribution of '+indice_name+' over Quebec'))
fig3.show()
fig3.savefig('/exec/yanncha/sea_ice/figures/tasmax_'+indice+'_'+season+'_global_distribution.png',dpi=300)
file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/statistics_tasmax.txt','a')
file_txt.write(('### Figure 1 done! (%d seconds)' % (tt.time() - start_time)))
file_txt.close()
