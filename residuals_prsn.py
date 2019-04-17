##################################################################
# Description:
# Code name: residuals_prsn.py
# Date of creation: 2019/002/19
# Date of last modification: 2019/02/19
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
path = ('/exec/yanncha/sea_ice/prsn/')
season = "SON"

### LOOP ON SIMULATIONS
for sim in simulations:

    # Opening relevant datasets
    filepath_d  = os.path.join(path, "prsn_detrended_{0}_{1}.nc".format(season,sim))
    ds_d        = xr.open_dataset(filepath_d)   # data detrended
    filepath_r  = os.path.join(path, "prsn_rearranged_{0}_{1}.nc".format(season,sim))
    ds_r        = xr.open_dataset(filepath_r)   # data non-detrended

    # Definition of residual characteristics
    if season == "DJFM":
        mean           = ds_d.resample(time='AS-DEC').reduce(np.nanmean)
        std            = ds_d.resample(time='AS-DEC').reduce(np.nanstd)
        sum_detr       = ds_d.resample(time='AS-DEC').reduce(np.nansum)
        sum_tr         = ds_r.resample(time='AS-DEC').reduce(np.nansum)
        sumrel         = sum_detr/(sum_tr-sum_detr)
    else:
        mean           = ds_d.resample(time='YS').reduce(np.nanmean)
        std            = ds_d.resample(time='YS').reduce(np.nanstd)
        sum_detr       = ds_d.resample(time='YS').reduce(np.nansum)
        sum_tr         = ds_r.resample(time='YS').reduce(np.nansum)
        sumrel         = sum_detr/(sum_tr-sum_detr)

    # Storing the results in a netcdf file
    mean.to_netcdf(('/exec/yanncha/sea_ice/prsn/prsn_mean_'+season+'_'+sim+'.nc'))
    std.to_netcdf(('/exec/yanncha/sea_ice/prsn/prsn_std_'+season+'_'+sim+'.nc'))
    sumrel.to_netcdf(('/exec/yanncha/sea_ice/prsn/prsn_sumrel_'+season+'_'+sim+'.nc'))

    # Closing all datasets
    ds_d.close()
    mean.close()
    std.close()
    sumrel.close()

    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/residuals_prsn.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)\n' % (tt.time() - start_time)))
    file_txt.close()
    print('### Simulation '+sim+' done! (%d seconds)\n' % (tt.time() - start_time))
    start_time = tt.time()
