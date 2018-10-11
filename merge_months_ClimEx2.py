##################################################################
# Description:
# Code name: merge_months_ClimEx.py
# Date of creation: 2018/10/09
# Date of last modification: 2018/10/09
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import os
import xarray as xr
import numpy as np
import sys

import functions_detrending as fct_d

import time as tt
start_time = tt.time()

# Initialization
#simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
#"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
#"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
#"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
simulations = ["kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu"]
var = "tasmax"
months = ("06","07","08","09")

### LOOP ON SIMULATIONS
for sim in simulations:

    # Selection of the paths and filenames corresponding to our criteria
    paths = fct_d.select_months(sim, months)
    filepaths = []
    for p in paths:
        month = p[-6:]
        filepaths.append(os.path.join(p, "{0}_{1}_{2}_se.nc".format(var, sim, month)))
    filepaths.sort()
    filepaths = filepaths[4:]

    # Merging timesteps by 16 litte spatial squares over Quebec
    # initialization of the data
    dataset     = xr.open_mfdataset(filepaths)

    # loop on the little squares
    lon_min     = [-80.,-74.,-68.,-62.,-80.,-74.,-68.,-62.,-80.,-74.,-68.,-62.,-80.,-74.,-68.,-62.]
    lon_max     = [-74.,-68.,-62.,-56.,-74.,-68.,-62.,-56.,-74.,-68.,-62.,-56.,-74.,-68.,-62.,-56.]
    lat_min     = [45.,45.,45.,45.,49.5,49.5,49.5,49.5,54.,54.,54.,54.,58.5,58.5,58.5,58.5]
    lat_max     = [49.5,49.5,49.5,49.5,54.,54.,54.,54.,58.5,58.5,58.5,58.5,63.,63.,63.,63.]

    for s in range(len(lon_min)):
        dsSub   = dataset.where((dataset.lon>=lon_min[s])&(dataset.lon<lon_max[s])&(dataset.lat>=lat_min[s])&(dataset.lat<lat_max[s]),drop=True)
        tasmax  = dsSub['tasmax'][:,:,:]
        tasmax.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_rearranged_'+sim+'_sq'+str(s)+'.nc'))
        print('# simulation '+sim+', square #'+str(s)+' done! (%d seconds)' % (tt.time() - start_time))
        start_time = tt.time()

    print('### Simulation '+sim+' done!')
#rlat    = dsSub['rlat'][:]
#rlon    = dsSub['rlon'][:]
#time    = dsSub['time'][:]
