##################################################################
# Description: ClimEx data is organized by months. In order to apply statistical
# computation, data needs to be merged.
# Code name: merge_months_tasmax.py
# Date of creation: 2018/10/09
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
#
simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk","kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx","kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek","kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
#months = ("06","07","08","09") # summer
#season = "JJAS"
months = ("04","05","06") # spring
season = "AMJ"

### LOOP ON CLIMEX SIMULATIONS
for sim in simulations:

    # Selection of the paths and filenames corresponding to our criteria
    paths = fct_d.select_months(sim, months)
    filepaths = []
    for p in paths:
        month = p[-6:]
        filepaths.append(os.path.join(p, "tasmax_{0}_{1}_se.nc".format(sim, month)))
    filepaths.sort()
    filepaths = filepaths[4:] # remove year 1954

    # Merging timesteps over a square englobing the Quebec province
    # initialization of the data
    dataset     = xr.open_mfdataset(filepaths)

    # loop on the little squares
    lon_min     = -80.
    lon_max     = -56.
    lat_min     = 45.
    lat_max     = 63.

    # extraction of subdata
    dsSub   = dataset.where((dataset.lon>=lon_min)&(dataset.lon<lon_max)&(dataset.lat>=lat_min)&(dataset.lat<lat_max),drop=True)
    tasmax  = dsSub['tasmax'][:,:,:]
    tasmax.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_rearranged_'+season+'_'+sim+'.nc'))
    dataset.close()
    dsSub.close()
    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/merge_months_tasmax.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time)))
    file_txt.close()
    print('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time))
    start_time = tt.time()
