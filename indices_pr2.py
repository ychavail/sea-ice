##################################################################
# Description:
# Code name: indices_pr.py
# Date of creation: 2019/01/14
# Date of last modification: 2019/01/15
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
start_time2 = tt.time()

# Initialization
simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
path = ('/exec/yanncha/sea_ice/pr/')
season = "DJFM"

### LOOP ON SIMULATIONS
for sim in simulations:

    # Opening relevant datasets
    filepath    = os.path.join(path, "pr_rearranged_{0}_{1}.nc".format(season,sim))
    filepath_d  = os.path.join(path, "pr_detrended_{0}_{1}.nc".format(season,sim))
    ds          = xr.open_dataset(filepath)     # data with trend
    ds_d        = xr.open_dataset(filepath_d)   # data detrended
    years_tmp   = np.array(ds.time.dt.year)
    years       = list(range(years_tmp[0],years_tmp[-1]+1))

    # Definition of indices
    # 1. maximum daily precipitation
    if season == "DJFM":
        max1j          = ds_d.resample(time='AS-DEC').max(dim='time')
    else:
        max1j          = ds_d.resample(time='YS').max(dim='time')
    for y in years:
        if season == "DJFM":
            dec     = ((ds_d.time.dt.year==y-1)&(ds_d.time.dt.month==12))
            jan     = ((ds_d.time.dt.year==y)&(ds_d.time.dt.month==1))
            fev     = ((ds_d.time.dt.year==y)&(ds_d.time.dt.month==2))
            mar     = ((ds_d.time.dt.year==y)&(ds_d.time.dt.month==3))
            ds_dy   = ds_d.where(dec | jan | fev | mar,drop=True)
        else:
            ds_dy   = ds_d.where((ds_d.time.dt.year==y),drop=True)
        # 2. maximum 5-day precipitation
        ds5_dy      = ds_dy.rolling(time=5,center=True).sum()
        max5j_y     = ds5_dy.max(dim="time")

        # adding a new time-axis where needed
        max5j_y.expand_dims('time')
        if y==years[0]:
            max5j          = max5j_y
        else:
            max5j          = xr.concat([max5j,max5j_y],dim='time')

        file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/indices_pr.txt','a')
        file_txt.write(('# sim '+sim+', year '+str(y)+' (%d seconds)\n' % (tt.time() - start_time)))
        file_txt.close()
        start_time = tt.time()

    max5j.assign_coords(time=years,dim='time')

    # Storing the indices in a netcdf file
    max1j.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_max1j_'+season+'_'+sim+'.nc'))
    max5j.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_max5j_'+season+'_'+sim+'.nc'))

    # Closing all datasets
    ds.close()
    ds_d.close()
    ds_dy.close()
    max5j_y.close()
    max1j.close()
    max5j.close()

    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/indices_pr.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)\n' % (tt.time() - start_time2)))
    file_txt.close()
    start_time2 = tt.time()
