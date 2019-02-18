##################################################################
# Description:
# Code name: fig_distribution_qqplot.py
# Date of creation: 2019/01/15
# Date of last modification: 2019/01/21
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
indice      = 'mean'
indice_name = 'seasonal mean value'
units       = 'T [K]'
scale       = 'global'
path        = '/exec/yanncha/sea_ice/'
seasons     = ['SON','DJFM','AMJ']
subplots    = [231,232,233,234,235,236]
colors      = ['r','#000090','#8A0808']
labels      = ['no ice','ice','unclear']
percs       = np.array([0.1,1,2,3,4,5,10,20,30,40,50,60,70,80,90,95,96,97,98,99,99.9])
plt_bnds    = [-10,10,0,0.6]
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
# pr mean [-4,4,0,1.4]
# pr std [0,20,0,0.3]
# pr max1j [0,150,0,0.06]
# pr max5j [0,200,0,0.04]
# pr sumrel [-100,100,0,0.025]
qq_bnds     = [-8,8,-8,8]
# tasmin mean [-8,8,-8,8]
# tasmin std [0,14,0,14]
# tasmax mean [-8,8,-8,8]
# tasmax std [0,14,0,14]
# tasmax maxx [0,25,0,25]
# tasmax qmax99 [0,25,0,25]
# tasmax qmax95 [0,25,0,25]
# pr mean [-3,3,-3,3]
# pr std [0,20,0,20]
# pr max1j [0,140,0,140]
# pr max5j [0,180,0,180]
# pr sumrel [-80,80,-80,80]

## Creating a mask on land
dataset     = xr.open_dataset('/klmx1/leduc/climex-core-qc/kay/195001/sftlf_kay_195001_se.nc')
lon_min     = -80.
lon_max     = -56.
lat_min     = 45.
lat_max     = 63.
dsSub       = dataset.where((dataset.lon>=lon_min)&(dataset.lon<lon_max)&(dataset.lat>=lat_min)&(dataset.lat<lat_max),drop=True)
sftlf       = np.array(dsSub['sftlf'][0,:,:])

## Figure initialization
fig1 = plt.figure(figsize=(18,12))

## Loop on seasons for distribution
for s in range(len(seasons)):
    ax = fig1.add_subplot(subplots[s])

    ## Loop on clusters
    for c in range(3):

        ## Loading file
        file        = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted'+str(c)+'.nc'
        nc          = netcdf.Dataset(file,'r')
        ind_        = nc.variables[indice][:,:,:].data
        if var != 'pr':
            land_mask	= np.zeros(ind_.shape, dtype=bool)
            land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
            ind_        = np.ma.array(ind_,mask=land_mask)
            ind         = ind_[~np.isnan(ind_)]
        else:
            ind         = 3600*ind_[~np.isnan(ind_)]

        ## Plotting
        if s == 0:
            sns.distplot(random.sample(list(ind.data), 20000),rug=False,hist=False,kde_kws={"color": colors[c], "label": labels[c]})
        else:
            sns.distplot(random.sample(list(ind.data), 20000),rug=False,hist=False,kde_kws={"color": colors[c]})

        del file,nc
        print('### DISTRIBUTION: Season '+seasons[s]+' with cluster <'+labels[c]+'> done! (%d seconds)' % (tt.time() - start_time))

    ## Plot customization
    #plt.axis(plt_bnds)
    plt.grid(color='#C0C0C0', linestyle='--', linewidth=1)
    ax.set_title(seasons[s],fontsize=15)
    if s == 0:
        ax.set_ylabel(indice_name+' of '+var,fontsize=15)
    if s == 1:
        ax.set_xlabel(units,fontsize=15)

## Loop on seasons for Qqplot
for s in range(len(seasons)):
    ax = fig1.add_subplot(subplots[s+3])

    ## Loading files
    file0       = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted0.nc'
    nc0         = netcdf.Dataset(file0,'r')
    ind0_       = nc0.variables[indice][:,:,:].data
    if var != 'pr':
        ind0_       = nc0.variables[indice][:,:,:].data
        land_mask	= np.zeros(ind0_.shape, dtype=bool)
        land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
        ind0        = ind0_[~np.isnan(ind0_)]
    else:
        ind0        = 3600*ind0_[~np.isnan(ind0_)]

    file1       = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted1.nc'
    nc1         = netcdf.Dataset(file1,'r')
    ind1_       = nc1.variables[indice][:,:,:].data
    if var != 'pr':
        land_mask	= np.zeros(ind1_.shape, dtype=bool)
        land_mask[:,:,:] 	= sftlf[np.newaxis,:,:] < 0.1
        ind1_       = np.ma.array(ind1_,mask=land_mask)
        ind1        = ind1_[~np.isnan(ind1_)]
    else:
        ind1        = 3600*ind1_[~np.isnan(ind1_)]


    ## Plotting
    qn0     = np.percentile(ind0, percs)
    qn1     = np.percentile(ind1, percs)
    plt.plot(qn0,qn1,ls='',marker='o',color='#8A0808')
    x = np.linspace(qq_bnds[0],qq_bnds[1])
    plt.plot(x,x, color='k', ls='--')
    #plt.axis(qq_bnds)
    plt.grid(color='#C0C0C0', linestyle='--', linewidth=1)
    if s == 0:
        ax.set_ylabel('with ice '+units,fontsize=15)
    if s == 1:
        ax.set_xlabel('without ice '+units,fontsize=15)
    print('### QQPLOT: Season '+seasons[s]+' done! (%d seconds)' % (tt.time() - start_time))

fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/fig_'+var+'_'+indice+'_'+scale+'_distribution_qqplot.png',dpi=300)
