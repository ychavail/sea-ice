##################################################################
# Description: ClimEx data is organized by months. In order to apply statistical
# computation, data needs to be merged.
# Code name: merge_months_pr.py
# Date of creation: 2018/10/12
# Date of last modification: 2018/10/12
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
simulations = ["kda"]
#simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
#"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
#"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
#"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
months = ("01","02","03","04","05","06","07","08","09","10","11","12") # entire year

### LOOP ON CLIMEX SIMULATIONS
for sim in simulations:

    # Selection of the paths and filenames corresponding to our criteria
    paths = fct_d.select_months(sim, months)
    filepaths = []
    for p in paths:
        month = p[-6:]
        filepaths.append(os.path.join(p, "pr_{0}_{1}_se.nc".format(sim, month)))
    filepaths.sort()
    filepaths = filepaths[12:] # remove year 1954
    filepaths_rs = np.resize(filepaths,(10,np.int(len(filepaths)/10)))


    # Merging timesteps over a square englobing the Quebec province
    # loop on the little square
    lon_min     = -80.
    lon_max     = -56.
    lat_min     = 45.
    lat_max     = 63.

    # initialization of the data
    #xr.set_options(enable_cftimeindex=True)
    for i in range(10):
        print('avant')
        dataset     = xr.open_mfdataset(filepaths_rs[i,:],drop_variables='time_bnds')
        print('apres')
        # extraction of subdata
        dsSub   = dataset.where((dataset.lon>=lon_min)&(dataset.lon<lon_max)&(dataset.lat>=lat_min)&(dataset.lat<lat_max),drop=True)
        print('dssub')
        dsDay   = dsSub.resample(time='24H').reduce(np.sum) # sum of hourly data to get daily data
        print('dsday')
        pr      = dsDay['pr'][:,:,:]
        print('pr')
        pr.to_netcdf(('/exec/yanncha/sea_ice/pr/pr_rearranged_'+sim+'_'+str(i+1)+'.nc'))
        print('netcdf')
        dataset.close()
        dsSub.close()
        dsDay.close()
        print('# Part '+str(i+1)+' done!')
    print('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time))
    start_time = tt.time()
