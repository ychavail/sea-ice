##################################################################
# Description: Code selecting all the merged (i.e. transformed) files from the
# ClimEx ensemble for a specific climate variable and specific months, masking the
# data over the Quebec province, detrending the climate change component
# saving a new netcdf-file for each of the 50 ClimEx simulations.
# Code name: detrend_prsn.py
# Date of creation: 2019/01/14
# Date of last modification: 2019/01/14
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import os
#import ocgis
#from ocgis import OcgOperations, RequestDataset, env
#from ocgis.test.base import create_gridxy_global, create_exact_field
import xarray as xr
import numpy as np
import functions_detrending as fct_d
import sys

import time as tt
start_time = tt.time()

# Initialization
simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
var = "prsn"
var_nc = ["prsn"]
season = "DJFM"
path = ('/exec/yanncha/sea_ice/'+var+'/')

### LOOP ON SIMULATIONS
for sim in simulations:

    filepath = os.path.join(path, "{0}_rearranged_{1}_{2}.nc".format(var, season, sim))
    dataset     = xr.open_dataset(filepath)
    var_        = dataset[var][:,:,:]
    time        = dataset['time'][:]
    rlat        = dataset['rlat'][:]
    rlon        = dataset['rlon'][:]
    lat         = dataset['lat'][:,:]
    lon         = dataset['lon'][:,:]

    # Removing the climate change tendancy from the data
    var_d    = np.empty([len(time),len(rlat),len(rlon)])
    for i in range(len(rlon)):
        for j in range(len(rlat)):
            var_ij = dataset[var][:,j,i]
            var_d[:,j,i] = fct_d.cubic_detrend(var_ij.values)
            #print('# i='+str(i)+' j='+str(j))

    # Defining a new xarray
    xr_new      = xr.Dataset({var: (['time','rlat','rlon'], var_d),
                              'lat': (['rlat','rlon'], lat),
                              'lon': (['rlat','rlon'], lon)},
                      coords={'time': (['time'], time),
                              'rlat': (['rlat'], rlat),
                              'rlon': (['rlon'], rlon)})

    # Storing the detrended data in a netcdf file
    xr_new.to_netcdf(('/exec/yanncha/sea_ice/'+var+'/'+var+'_detrended_'+season+'_'+sim+'.nc'))
    dataset.close()
    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/detrend_'+var+'.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time)))
    file_txt.close()
    print('### Simulation '+sim+' done! (%d seconds)' % (tt.time() - start_time))
    start_time = tt.time()
