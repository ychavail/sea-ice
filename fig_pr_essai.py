##################################################################
# Description:
# Code name:
# Date of creation: 2019/01/30
# Date of last modification: 2019/01/30
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
infinity	= 'max'
palette		= plt.cm.seismic
levels		= [1,20,40,60,80,100,120,140,160,180,200]
# pour mean: [-4,-3,-2,-1,0,1,2,3,4]

ds_r        = xr.open_dataset('/exec/yanncha/sea_ice/pr/pr_rearranged_DJFM_kda.nc')
sum         = ds_r.resample(time='AS-DEC').reduce(np.nansum)
cumul=np.array(sum.pr)*864
lons=np.array(sum.lon)
lats=np.array(sum.lat)

fig1 = plt.figure(figsize=(6,6))
im = fct_p.map_contourfQC(fig1,111,np.mean(cumul,axis=0),lons,lats,'DJFM','cumul moyen kda',levels,infinity,palette)
fig1.subplots_adjust(right=0.8)
cbar_ax = fig1.add_axes([0.85, 0.3, 0.01, 0.4])
fig1.colorbar(im,cax=cbar_ax)
fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/fig_essai_pr.png',dpi=300)
