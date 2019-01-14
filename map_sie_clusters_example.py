##################################################################
# Description: Plot a map of sea ice extent for a randomly chosen september in each cluster.
# Code name: map_sie_clusters_example.py
# Date of creation: 2018/11/22
# Date of last modification: 2018/11/22
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as netcdf
import functions_plot as fct_p
import functions_time as fct_t
import sys

# File .npy with definition of clusters
clusters    = np.load('/exec/yanncha/sea_ice/clusters/sic_september_clusters_kmeans_CanESM2-LE.npy')

# Random choice of sample for each cluster
cluster     = clusters[:,5]
ind0        = np.where(cluster=='0')
ind1        = np.where(cluster=='1')
ind2        = np.where(cluster=='2')
rand0       = np.random.randint(len(ind0[0]), size=1)
rand1       = np.random.randint(len(ind1[0]), size=1)
rand2       = np.random.randint(len(ind2[0]), size=1)
fam0        = clusters[ind0[0][rand0][0],0]
mem0        = clusters[ind0[0][rand0][0],1]
year0       = clusters[ind0[0][rand0][0],3]
fam1        = clusters[ind1[0][rand1][0],0]
mem1        = clusters[ind1[0][rand1][0],1]
year1       = clusters[ind1[0][rand1][0],3]
fam2        = clusters[ind2[0][rand2][0],0]
mem2        = clusters[ind2[0][rand2][0],1]
year2       = clusters[ind2[0][rand2][0],3]

# Loading file with sea ice extent data
if int(year0) <= 2020:
    nc0     = netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r'+fam0+'/day/seaIce/sic/r'+mem0+'i1p1/sic_day_CanESM2_historical-r'+fam0+'_r'+mem0+'i1p1_19500101-20201231.nc','r')
else:
    nc0     = netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r'+fam0+'/day/seaIce/sic/r'+mem0+'i1p1/sic_day_CanESM2_historical-r'+fam0+'_r'+mem0+'i1p1_20210101-21001231.nc','r')
if int(year1) <= 2020:
    nc1     = netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r'+fam1+'/day/seaIce/sic/r'+mem1+'i1p1/sic_day_CanESM2_historical-r'+fam1+'_r'+mem1+'i1p1_19500101-20201231.nc','r')
else:
    nc1     = netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r'+fam1+'/day/seaIce/sic/r'+mem1+'i1p1/sic_day_CanESM2_historical-r'+fam1+'_r'+mem1+'i1p1_20210101-21001231.nc','r')
if int(year2) <= 2020:
    nc2     = netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r'+fam2+'/day/seaIce/sic/r'+mem2+'i1p1/sic_day_CanESM2_historical-r'+fam2+'_r'+mem2+'i1p1_19500101-20201231.nc','r')
else:
    nc2     = netcdf.Dataset('/dmf2/scenario/external_data/cccma/CanESM2_large_ensemble/historical-r'+fam2+'/day/seaIce/sic/r'+mem2+'i1p1/sic_day_CanESM2_historical-r'+fam2+'_r'+mem2+'i1p1_20210101-21001231.nc','r')


# Defining variables
lat	    = nc0.variables['lat'][32:]
lon	    = nc0.variables['lon'][:]
time0   = nc0.variables['time']
time1   = nc1.variables['time']
time2   = nc2.variables['time']
indt0   = fct_t.selmonthyear(int(year0),9,time0[:],time0.units,time0.calendar)
indt1   = fct_t.selmonthyear(int(year1),9,time1[:],time1.units,time1.calendar)
indt2   = fct_t.selmonthyear(int(year2),9,time2[:],time2.units,time2.calendar)
sic0	= np.nanmean(nc0.variables['sic'][indt0[0],32:,:],axis=0)
sic1	= np.nanmean(nc1.variables['sic'][indt1[0],32:,:],axis=0)
sic2	= np.nanmean(nc2.variables['sic'][indt2[0],32:,:],axis=0)


# Plotting maps
levels		= [0,10,20,30,40,50,60,70,80,90,100]
palette		= plt.cm.YlGnBu
infinity	= 'neither'
fig1		= plt.figure(figsize=(14.4,5))
im = fct_p.map_contourfAR(fig1,131,sic0,lon,lat,('no ice - r'+fam0+'-'+mem0+' '+year0),"",levels,infinity,palette)
im = fct_p.map_contourfAR(fig1,132,sic1,lon,lat,('ice - r'+fam1+'-'+mem1+' '+year1),"",levels,infinity,palette)
im = fct_p.map_contourfAR(fig1,133,sic2,lon,lat,('unclear - r'+fam2+'-'+mem2+' '+year2),"",levels,infinity,palette)
fig1.subplots_adjust(right=0.8)
cbar_ax = fig1.add_axes([0.85, 0.3, 0.01, 0.4])
cbar_ax.set_xlabel('[%]', rotation=0,fontsize=7)
fig1.colorbar(im,cax=cbar_ax)
fig1.suptitle('Sea ice cover [%] in september from CanESM2-LE', fontsize=10)
fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/map_sie_clusters_example.png',dpi=300)
