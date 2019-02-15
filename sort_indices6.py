##################################################################
# Description: Works also for residuals.
# Code name: sort_indices.py
# Date of creation: 2018/10/24
# Date of last modification: 2018/11/15
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import numpy as np
import xarray as xr
import os
import sys
import time as tt
#import xclim as xc
start_time = tt.time()
start_time2 = tt.time()

# Initialization
clim_var    = "pr"
indice      = "sumrel"
season      = "SON"
simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
path = ('/exec/yanncha/sea_ice/'+clim_var+'/')

# File .npy with definition of clusters
# col0: family, col1: member CanESM2-LE, col2: member ClimEx, col3: year,
# col4: sea ice extent, col5: cluster class (0 no ice, 1 ice, 2 unsure)
clusters    = np.load('/exec/yanncha/sea_ice/clusters/sic_september_clusters_kmeans_CanESM2-LE.npy')
member      = clusters[:,2]
year        = clusters[:,3]
cluster     = clusters[:,5]

# Initatialization of new variables
member0     = []
years0      = []
member1     = []
years1      = []
member2     = []
years2      = []
i0          = 0
i1          = 0
i2          = 0

### LOOP ON SIMULATIONS
for sim in simulations:
    # load file with indice
    filepath    = os.path.join(path, "{0}_{1}_{2}_{3}.nc".format(clim_var,indice,season,sim))
    ds          = xr.open_dataset(filepath)
    if season == "SON":
        years = np.array(range(1955,2100))
    else:
        years = np.array(range(1954,2099))

    # loop on years
    for y in years:
        ind     = np.intersect1d(np.where(member==sim),np.where(year==str(y)))
        group   = cluster[ind]

        # adding the map to the corresponding cluster
        if group[0]=='0':
            member0.append(sim)
            years0.append(y)
            ind0_y  = np.expand_dims(np.array(ds[clim_var][np.where(years==y)[0][0],:,:]), axis=0)
            if i0 == 0:
                indice0 = ind0_y
            else:
                indice0 = np.concatenate((indice0,ind0_y),axis=0)
            i0 += 1
        if group[0]=='1':
            member1.append(sim)
            years1.append(y)
            ind1_y  = np.expand_dims(np.array(ds[clim_var][np.where(years==y)[0][0],:,:]), axis=0)
            if i1 == 0:
                indice1 = ind1_y
            else:
                indice1 = np.concatenate((indice1,ind1_y),axis=0)
            i1 += 1
        if group[0]=='2':
            member2.append(sim)
            years2.append(y)
            ind2_y  = np.expand_dims(np.array(ds[clim_var][np.where(years==y)[0][0],:,:]), axis=0)
            if i2 == 0:
                indice2 = ind2_y
            else:
                indice2 = np.concatenate((indice2,ind2_y),axis=0)
            i2 += 1

    file_txt = open('/home/yanncha/GitHub/sea-ice/outputs_from_code/sort_indices.txt','a')
    file_txt.write(('### Simulation '+sim+' done!\n'))
    file_txt.close()
    print('### Simulation '+sim+' done!')

# Defining a new xarray
rlat        = ds['rlat'][:]
rlon        = ds['rlon'][:]
lat         = ds['lat'][:,:]
lon         = ds['lon'][:,:]
time0       = list(range(len(years0)))
time1       = list(range(len(years1)))
time2       = list(range(len(years2)))

xr_0        = xr.Dataset({indice: (['time','rlat','rlon'], indice0),
                              'member': (['time'], member0),
                              'years': (['time'], years0),
                              'lat': (['rlat','rlon'], lat),
                              'lon': (['rlat','rlon'], lon)},
                      coords={'time': (['time'], time0),
                              'rlat': (['rlat'], rlat),
                              'rlon': (['rlon'], rlon)})

xr_1        = xr.Dataset({indice: (['time','rlat','rlon'], indice1),
                              'member': (['time'], member1),
                              'years': (['time'], years1),
                              'lat': (['rlat','rlon'], lat),
                              'lon': (['rlat','rlon'], lon)},
                      coords={'time': (['time'], time1),
                              'rlat': (['rlat'], rlat),
                              'rlon': (['rlon'], rlon)})

xr_2        = xr.Dataset({indice: (['time','rlat','rlon'], indice2),
                              'member': (['time'], member2),
                              'years': (['time'], years2),
                              'lat': (['rlat','rlon'], lat),
                              'lon': (['rlat','rlon'], lon)},
                      coords={'time': (['time'], time2),
                              'rlat': (['rlat'], rlat),
                              'rlon': (['rlon'], rlon)})


# Storing the indices in a netcdf file
xr_0.to_netcdf(('/exec/yanncha/sea_ice/'+clim_var+'/'+clim_var+'_'+indice+'_'+season+'_sorted0.nc'))
xr_1.to_netcdf(('/exec/yanncha/sea_ice/'+clim_var+'/'+clim_var+'_'+indice+'_'+season+'_sorted1.nc'))
xr_2.to_netcdf(('/exec/yanncha/sea_ice/'+clim_var+'/'+clim_var+'_'+indice+'_'+season+'_sorted2.nc'))
