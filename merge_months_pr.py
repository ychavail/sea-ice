##################################################################
# Description: ClimEx data is organized by months. In order to apply statistical
# computation, data needs to be merged.
# Code name: merge_months_pr.py
# Date of creation: 2019/01/14
# Date of last modification: 2019/01/14
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import os
import xarray as xr
import numpy as np
import sys
import glob

import functions_detrending as fct_d

import time as tt
start_time = tt.time()

# Initialization
input_path  = '/exec/yanncha/sea_ice/pr/daily/'
output_path = '/exec/yanncha/sea_ice/pr/'
simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk","kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx","kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek","kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
months = (4,5,6)
season = "AMJ"

### LOOP ON CLIMEX SIMULATIONS
for sim in simulations:

    # selection of the filenames corresponding to our criteria
    filepaths   = glob.glob(input_path+'pr_daily_'+sim+'*')

    # initialization of the data for the selected season
    dataset     = xr.open_mfdataset(filepaths)
    if np.size(months)==3:
        dsSub       = dataset.where((dataset['time.month']==months[0]) | (dataset['time.month']==months[1]) | (dataset['time.month']==months[2]),drop=True)
    elif np.size(months)==4:
        dsSub       = dataset.where((dataset['time.month']==months[0]) | (dataset['time.month']==months[1]) | (dataset['time.month']==months[2]) | (dataset['time.month']==months[3]),drop=True)

    # writing data in a new netcdf file
    pr  = dsSub['pr'][:,:,:]
    pr.to_netcdf((output_path+'/pr_rearranged_'+season+'_'+sim+'.nc'))
    dataset.close()
    dsSub.close()
    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/merge_months_pr.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time)))
    file_txt.close()
    print('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time))
    start_time = tt.time()
