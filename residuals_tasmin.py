##################################################################
# Description:
# Code name: residuals_tasmin.py
# Date of creation: 2018/11/14
# Date of last modification: 2018/11/14
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# doit travailler dans l'environnement virtuel xcenv pour xclim

# Needed packages
import os
import xarray as xr
import xclim as xc
import numpy as np
import sys
import time as tt
start_time = tt.time()

# Initialization
simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
path = ('/exec/yanncha/sea_ice/tasmin/')
season = "AMJ"

### LOOP ON SIMULATIONS
for sim in simulations:

    # Opening relevant datasets
    filepath_d  = os.path.join(path, "tasmin_detrended_{0}_{1}.nc".format(season,sim))
    ds_d        = xr.open_dataset(filepath_d)   # data detrended

    # Definition of residual characteristics
    if season == "DJFM":
        mean           = ds_d.resample(time='AS-DEC').reduce(np.nanmean)
        std            = ds_d.resample(time='AS-DEC').reduce(np.nanstd)
    else:
        mean           = ds_d.resample(time='YS').reduce(np.nanmean)
        std            = ds_d.resample(time='YS').reduce(np.nanstd)

    # Storing the results in a netcdf file
    mean.to_netcdf(('/exec/yanncha/sea_ice/tasmin/tasmin_mean_'+season+'_'+sim+'.nc'))
    std.to_netcdf(('/exec/yanncha/sea_ice/tasmin/tasmin_std_'+season+'_'+sim+'.nc'))

    # Closing all datasets
    ds_d.close()
    mean.close()
    std.close()

    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/residuals_tasmin.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)\n' % (tt.time() - start_time)))
    file_txt.close()
    print('### Simulation '+sim+' done! (%d seconds)\n' % (tt.time() - start_time))
    start_time = tt.time()
