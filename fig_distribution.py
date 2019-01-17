##################################################################
# Description:
# Code name: fig_distribution.py
# Date of creation: 2019/01/15
# Date of last modification: 2019/01/17
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import netCDF4 as netcdf
import seaborn as sns
import random
import sys
import time as tt
start_time = tt.time()

## Initialization
var         = 'tasmax'
indice      = 'qmax95'
indice_name = 'seasonal 95th percentile'
units       = 'T [K]'
scale       = 'global'
path        = '/exec/yanncha/sea_ice/'
seasons     = ['SON','DJFM','AMJ']
subplots    = [131,132,133]
colors      = ['r','#000090','#8A0808']
labels      = ['no ice','ice','unclear']
plt_bnds    = [-5,40,0,0.14]

# tasmin mean [-10,10,0,0.6]
# tasmin std [0,15,0,0.35]
# tasmin minn [-40,5,0,0.14]
# tasmin qmin01 [-40,5,0,0.14]
# tasmin qmin05 [-40,5,0,0.14]
# tasmax mean [-10,10,0,0.6]
# tasmax std [0,15,0,0.35]
# tasmax maxx [-5,40,0,0.14]
# tasmax qmax99 [-5,40,0,0.14]
# tasmax qmax95 [-5,40,0,0.14]

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
    ax = fig1.add_subplot(subplots[s])

    ## Loop on clusters
    for c in range(3):

        ## Loading file
        file        = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted'+str(c)+'.nc'
        nc          = netcdf.Dataset(file,'r')
        ind_        = nc.variables[indice][:,:,:].data
        land_mask	= np.zeros(ind_.shape, dtype=bool)
        land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
        ind_        = np.ma.array(ind_,mask=land_mask)
        ind         = ind_[~np.isnan(ind_)]

        ## Plotting
        if s == 0:
            sns.distplot(random.sample(list(ind.data), 20000),rug=False,hist=False,kde_kws={"color": colors[c], "label": labels[c]})
        else:
            sns.distplot(random.sample(list(ind.data), 20000),rug=False,hist=False,kde_kws={"color": colors[c]})

        del file,nc
        print('### Season '+seasons[s]+' with cluster <'+labels[c]+'> done! (%d seconds)' % (tt.time() - start_time))

    ## Plot customization
    plt.axis(plt_bnds)
    plt.grid(color='#C0C0C0', linestyle='--', linewidth=1)
    ax.set_title(seasons[s],fontsize=15)
    if s == 0:
        ax.set_ylabel(indice_name+' of '+var,fontsize=15)
    if s == 1:
        ax.set_xlabel(units,fontsize=15)

fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/fig_'+var+'_'+indice+'_'+scale+'_distribution.png',dpi=300)
