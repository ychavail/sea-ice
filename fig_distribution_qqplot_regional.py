##################################################################
# Description:
# Code name: fig_distribution_qqplot_regional.py
# Date of creation: 2019/02/05
# Date of last modification: 2019/02/05
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
var         = 'tasmin'
indice      = 'mean'
indice_name = 'seasonal mean value'
units       = 'T [K]'
scale       = 'MTL'
path        = '/exec/yanncha/sea_ice/'
seasons     = ['SON','DJFM','AMJ']
subplots    = [231,232,233,234,235,236]
colors      = ['r','#000090','#8A0808']
labels      = ['no ice','ice','unclear']
percs       = np.array([0.1,1,2,3,4,5,10,20,30,40,50,60,70,80,90,95,96,97,98,99,99.9])
plt_bnds    = [-10,10,0,0.6]
# MTL tasmax mean [-6,6,0,0.4]
# MTL tasmax maxx [0,30,0,0.18]
# MTL tasmax qmax99 [0,30,0,0.20]
# MTL tasmax qmax95 [0,25,0,0.25]
qq_bnds     = [-8,8,-8,8]
# MTL tasmax mean [-6,6,-6,6]
# MTL tasmax maxx [5,30,5,30]
# MTL tasmax qmax99 [5,30,5,30]
# MTL tasmax qmax95 [0,25,0,25]

## Figure initialization
fig1 = plt.figure(figsize=(18,12))

## Loop on seasons for distribution
for s in range(len(seasons)):
    ax = fig1.add_subplot(subplots[s])

    ## Loop on clusters
    for c in range(3):

        ## Loading file
        file        = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted'+str(c)+'_'+scale+'.nc'
        nc          = netcdf.Dataset(file,'r')
        ind_        = nc.variables[indice][:,:,:].data
        ind         = ind_[~np.isnan(ind_)]

        ## Plotting
        if s == 0:
            sns.distplot(ind,rug=False,hist=False,kde_kws={"color": colors[c], "label": labels[c]})
        else:
            sns.distplot(ind,rug=False,hist=False,kde_kws={"color": colors[c]})

        del file,nc
        print('### DISTRIBUTION: Season '+seasons[s]+' with cluster <'+labels[c]+'> done! (%d seconds)' % (tt.time() - start_time))

    ## Plot customization
    plt.axis(plt_bnds)
    plt.grid(color='#C0C0C0', linestyle='--', linewidth=1)
    ax.set_title(seasons[s],fontsize=15)
    if s == 0:
        ax.set_ylabel(indice_name+' of '+var+' in '+scale,fontsize=15)
    if s == 1:
        ax.set_xlabel(units,fontsize=15)

## Loop on seasons for Qqplot
for s in range(len(seasons)):
    ax = fig1.add_subplot(subplots[s+3])

    ## Loading files
    file0       = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted0_'+scale+'.nc'
    nc0         = netcdf.Dataset(file0,'r')
    ind0_       = nc0.variables[indice][:,:,:].data
    ind0        = ind0_[~np.isnan(ind0_)]
    file1       = path+var+'/'+var+'_'+indice+'_'+seasons[s]+'_sorted1_'+scale+'.nc'
    nc1         = netcdf.Dataset(file1,'r')
    ind1_       = nc1.variables[indice][:,:,:].data
    ind1        = ind1_[~np.isnan(ind1_)]

    ## Plotting
    qn0     = np.percentile(ind0, percs)
    qn1     = np.percentile(ind1, percs)
    plt.plot(qn0,qn1,ls='',marker='o',color='#8A0808')
    x = np.linspace(qq_bnds[0],qq_bnds[1])
    plt.plot(x,x, color='k', ls='--')
    plt.axis(qq_bnds)
    plt.grid(color='#C0C0C0', linestyle='--', linewidth=1)
    if s == 0:
        ax.set_ylabel('with ice '+units,fontsize=15)
    if s == 1:
        ax.set_xlabel('without ice '+units,fontsize=15)
    print('### QQPLOT: Season '+seasons[s]+' done! (%d seconds)' % (tt.time() - start_time))

fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/fig_'+var+'_'+indice+'_'+scale+'_distribution_qqplot.png',dpi=300)
