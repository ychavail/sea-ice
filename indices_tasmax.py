##################################################################
# Description:
# Code name: indices_tasmax.py
# Date of creation: 2018/10/19
# Date of last modification: 2018/10/23
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
path = ('/exec/yanncha/sea_ice/tasmax/')

### LOOP ON SIMULATIONS
for sim in simulations:

    # Opening relevant datasets
    filepath    = os.path.join(path, "tasmax_rearranged_{0}.nc".format(sim))
    filepath_d  = os.path.join(path, "tasmax_detrended_{0}.nc".format(sim))
    ds          = xr.open_dataset(filepath)     # data with trend
    ds_d        = xr.open_dataset(filepath_d)   # data detrended
    years_tmp   = np.array(ds.time.dt.year)
    years       = list(range(years_tmp[0],years_tmp[-1]+1))

    # Definition of indices
    # 1. maximum tasmax every summer
    maxx            = ds_d.resample(time='YS').max(dim='time')
    for y in years:
        ds_dy       = ds_d.where(ds_d.time.dt.year==y,drop=True)
        # 2. 95th percentile fo tasmax every summer
        qmax95_y    = ds_dy.quantile(0.95,dim="time")
        # 3. 99th percentile fo tasmax every summer
        qmax99_y    = ds_dy.quantile(0.99,dim="time")

        # adding a new time-axis where needed
        qmax95_y.expand_dims('time')
        qmax99_y.expand_dims('time')
        if y==years[0]:
            qmax95          = qmax95_y
            qmax99          = qmax99_y
        else:
            qmax95          = xr.concat([qmax95,qmax95_y],dim='time')
            qmax99          = xr.concat([qmax99,qmax99_y],dim='time')

        file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/indices_tasmax.txt','a')
        file_txt.write(('# sim '+sim+', year '+str(y)+' (%d seconds)\n' % (tt.time() - start_time)))
        file_txt.close()
        start_time = tt.time()

    qmax95.assign_coords(time=years,dim='time')
    qmax99.assign_coords(time=years,dim='time')

    # Storing the indices in a netcdf file
    maxx.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_maxx_'+sim+'.nc'))
    qmax95.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_qmax95_'+sim+'.nc'))
    qmax99.to_netcdf(('/exec/yanncha/sea_ice/tasmax/tasmax_qmax99_'+sim+'.nc'))

    # Closing all datasets
    ds.close()
    ds_d.close()
    ds_dy.close()
    qmax95_y.close()
    qmax99.close()
    maxx.close()
    qmax95.close()
    qmax99.close()

    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/indices_tasmax.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)\n' % (tt.time() - start_time2)))
    file_txt.close()
    start_time2 = tt.time()
