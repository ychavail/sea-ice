##################################################################
# Description: ClimEx data is organized by months. In order to apply statistical
# computation, data needs to be merged.
# Code name: merge_months_prsn.py
# Date of creation: 2019/01/18
# Date of last modification: 2019/01/21
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
simulations = ["kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx","kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek","kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
#months = ("06","07","08","09") # summer
#season = "JJAS"
months = ("12","01","02","03") # spring
season = "DJFM"


### TIME AXIS FROM TASMAX
paths = fct_d.select_months(simulations[0], months)
filepaths_tx = []
for p in paths:
    month = p[-6:]
    filepaths_tx.append(os.path.join(p, "tasmax_{0}_{1}_se.nc".format(simulations[0], month)))
filepaths_tx.sort()
filepaths_tx = filepaths_tx[4:]
ds_tx       = xr.open_mfdataset(filepaths_tx)
time_tx     = ds_tx.time
ds_tx.close()

### LOOP ON CLIMEX SIMULATIONS
for sim in simulations:

    # Selection of the paths and filenames corresponding to our criteria
    paths = fct_d.select_months(sim, months)
    filepaths = []
    for p in paths:
        month = p[-6:]
        filepaths.append(os.path.join(p, "prsn_{0}_{1}_se.nc".format(sim, month)))
    filepaths.sort()
    filepaths = filepaths[4:] # remove year 1954

    # Merging timesteps over a square englobing the Quebec province
    # initialization of the data
    dataset     = xr.open_mfdataset(filepaths,decode_times=False,drop_variables="time")
    dataset['time'] = time_tx

    # loop on the little squares
    lon_min     = -80.
    lon_max     = -56.
    lat_min     = 45.
    lat_max     = 63.

    # extraction of subdata
    dsSub   = dataset.where((dataset.lon>=lon_min)&(dataset.lon<lon_max)&(dataset.lat>=lat_min)&(dataset.lat<lat_max),drop=True)
    prsn  = dsSub['prsn'][:,:,:]
    prsn.to_netcdf(('/exec/yanncha/sea_ice/prsn/prsn_rearranged_'+season+'_'+sim+'.nc'))
    dataset.close()
    dsSub.close()
    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/merge_months_prsn.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time)))
    file_txt.close()
    print('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time))
    start_time = tt.time()
