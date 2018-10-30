##################################################################
# Description:
# Code name: indices_tasmin.py
# Date of creation: 2018/10/23
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
path = ('/exec/yanncha/sea_ice/tasmin/')

### LOOP ON SIMULATIONS
for sim in simulations:

    # Opening relevant datasets
    filepath    = os.path.join(path, "tasmin_rearranged_{0}.nc".format(sim))
    filepath_d  = os.path.join(path, "tasmin_detrended_{0}.nc".format(sim))
    ds          = xr.open_dataset(filepath)     # data with trend
    ds_d        = xr.open_dataset(filepath_d)   # data detrended
    years_tmp   = np.array(ds.time.dt.year) #########
    years       = list(range(years_tmp[0],years_tmp[-1]+1))

    # Definition of indices
    # 1. minimum tasmin every winter
    minn            = ds_d.resample(time='AS-DEC').min(dim='time')

    for y in years:
        dec     = ((ds_d.time.dt.year==y-1)&(ds_d.time.dt.month==12))
        jan     = ((ds_d.time.dt.year==y)&(ds_d.time.dt.month==1))
        fev     = ((ds_d.time.dt.year==y)&(ds_d.time.dt.month==2))
        mar     = ((ds_d.time.dt.year==y)&(ds_d.time.dt.month==3))
        ds_dy       = ds_d.where(dec | jan | fev | mar,drop=True)

        # 2. 5th percentile fo tasmin every winter
        qmin05_y    = ds_dy.quantile(0.05,dim="time")
        # 3. 1st percentile fo tasmax every winter
        qmin01_y    = ds_dy.quantile(0.01,dim="time")

        # adding a new time-axis where needed
        qmin05_y.expand_dims('time')
        qmin01_y.expand_dims('time')
        if y==years[0]:
            qmin05          = qmin05_y
            qmin01          = qmin01_y
        else:
            qmin05          = xr.concat([qmin05,qmin05_y],dim='time')
            qmin01          = xr.concat([qmin01,qmin01_y],dim='time')

        file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/indices_tasmin.txt','a')
        file_txt.write(('# sim '+sim+', year '+str(y)+' (%d seconds)\n' % (tt.time() - start_time)))
        file_txt.close()
        start_time = tt.time()

    qmin05.assign_coords(time=years,dim='time')
    qmin01.assign_coords(time=years,dim='time')

    # Storing the indices in a netcdf file
    minn.to_netcdf(('/exec/yanncha/sea_ice/tasmin/tasmin_minn_'+sim+'.nc'))
    qmin05.to_netcdf(('/exec/yanncha/sea_ice/tasmin/tasmin_qmin05_'+sim+'.nc'))
    qmin01.to_netcdf(('/exec/yanncha/sea_ice/tasmin/tasmin_qmin01_'+sim+'.nc'))

    # Closing all datasets
    ds.close()
    ds_d.close()
    ds_dy.close()
    qmin05_y.close()
    qmin01_y.close()
    minn.close()
    qmin05.close()
    qmin01.close()

    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/indices_tasmin.txt','a')
    file_txt.write(('### Simulation '+sim+' done! (%d seconds)\n' % (tt.time() - start_time2)))
    file_txt.close()
    start_time2 = tt.time()
