##################################################################
# Description:
# Code name: histogram_clusters.py
# Date of creation: 2018/11/15
# Date of last modification: 2018/11/15
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

# File .npy with definition of clusters
# col0: family, col1: member CanESM2-LE, col2: member ClimEx, col3: year,
# col4: sea ice extent, col5: cluster class (0 no ice, 1 ice, 2 unsure)
clusters    = np.load('/exec/yanncha/sea_ice/clusters/sic_september_clusters_kmeans_CanESM2-LE.npy')
year        = clusters[:,3].astype(int)
years       = np.unique(year)
cluster     = clusters[:,5]

occ         = np.zeros((3, len(years)))
for y in years:
    cluster_y           = cluster[np.where(year==y)]
    occ[0,y-years[0]]   = list(cluster_y).count('0')
    occ[1,y-years[0]]   = list(cluster_y).count('1')
    occ[2,y-years[0]]   = list(cluster_y).count('2')

# plotting stats
fig1 = plt.figure(figsize=(7.2,5.1))
plt.plot(years,occ[0,:]/np.sum(occ,axis=0)*100,ls='-',marker='',color='r',label='no ice')
plt.plot(years,occ[1,:]/np.sum(occ,axis=0)*100,ls='-',marker='',color='#000090',label='ice')
plt.plot(years,occ[2,:]/np.sum(occ,axis=0)*100,ls='-',marker='',color='#8A0808',label='unclear')
plt.title(('Distribution of clusters over time'))
plt.ylabel('[%]')
plt.legend()
plt.axis([1950,2100,-1,101])
fig1.show()
fig1.savefig('/exec/yanncha/sea_ice/figures/clusters_time_distribution.png',dpi=300)

# histogram
y_bnds = np.array([1950,1970,1990,2010,2030,2050,2070,2100])
x = np.array([1.,2.,3.,4.,5.,6.,7.])
occ_hist = np.zeros((3,len(y_bnds)-1))
for b in range(len(y_bnds)-1):
     occ_hist[:,b]      = np.sum(occ[:,np.intersect1d(np.where(years>=y_bnds[b]),np.where(years<y_bnds[b+1]))],axis=1)
fig2 = plt.figure(figsize=(7.2,5.1))
plt.bar(x-0.2,occ_hist[0,:],width=0.2,color='r',align='center',label='no ice')
plt.bar(x,occ_hist[1,:],width=0.2,color='#000090',align='center',label='ice')
plt.bar(x+0.2,occ_hist[2,:],width=0.2,color='#8A0808',align='center',label='unclear')
plt.ylabel('number of occurrences')
plt.xticks([1,2,3,4,5,6,7],("1950-1969","1970-1989","1990-2009","2010-2029","2030-2049","2050-2069","2070-2100"),fontsize=9)
plt.legend(loc='best')
plt.title(('Distribution of clusters over time'))
plt.axis([0.5,7.5,0,1600])
fig2.show()
fig2.savefig('/exec/yanncha/sea_ice/figures/clusters_time_historgram.png',dpi=300)
