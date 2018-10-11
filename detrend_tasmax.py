##################################################################
# Description: Code selecting all the merged (i.e. transformed) files from the
# ClimEx ensemble for a specific climate variable and specific months, masking the
# data over the Quebec province, detrending the climate change component
# saving a new netcdf-file for each of the 50 ClimEx simulations.
# Code name: detrend_tasmax.py
# Date of creation: 2018/10/04
# Date of last modification: 2018/10/10
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


# Initialization
#simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
#"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
#"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
#"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
simulations = ["kda"]
var = "tasmax"
var_nc = ["tasmax"]
path = ('/exec/yanncha/sea_ice/'+var+'/')

### LOOP ON SIMULATIONS
for sim in simulations:

    # LOOP ON LITTLE SPATIAL SQUARES
    for sq in range(16):
        filepath = os.path.join(path, "{0}_rearranged_{1}_sq{2}.nc".format(var, sim, str(sq)))
        dataset     = xr.open_dataset(filepath)
        tasmax      = dataset['tasmax'][:,:,:]
        time        = dataset['time'][:]
        rlat        = dataset['rlat'][:]
        rlon        = dataset['rlon'][:]

        # Removing the climate change tendancy from the data
        tasmax_d    = np.empty([len(time),len(rlat),len(rlon)])
        for i in range(len(rlon)):
            for j in range(len(rlat)):
                tasmax_ij = dataset['tasmax'][:,j,i]
                tasmax_d[:,j,i] = fct_d.cubic_detrend(tasmax_ij.values)
                print('# i='+str(i)+' j='+str(j))

        # Storing the detrended data in a netcdf file
        tasmax_d.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_detrended_'+sim+'_sq'+str(sq)+'.nc'))
        print('## Square '+str(sq)+' done...')
    print('### Simulation '+sim+' done!')
