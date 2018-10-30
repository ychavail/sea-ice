##################################################################
# Description: Functions enabling to fetch in the ClimEx database, gather releavant data and apply a detrend (climate change) on it.
# Code name: functions_detrending.py
# Date of creation: 2018/09/19
# Date of last modification: 2018/09/20
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import os
import numpy as np
import fnmatch
import netCDF4 as netcdf


# select_months: function that select a simulation from the ClimEx ensemble and picked folders corresponding to specific months ('m1','m2',...)
def select_months(simulation,months):
    path                = ('/klmx1/leduc/climex-core-qc/'+simulation+'/series/')
    all_months          = [x[0] for x in os.walk(path)]
    selected_months     = []

    for m in all_months:
        if m.endswith(months) == True:
            selected_months.append(m)

    return selected_months


# apply_maskQC: function that applies a mask on spatial data selecting grid points over the Quebec province of Canada
#def apply_maskQC():
    # no idea how to do it for now

# cubic_detrend: function that estimates a cubic polynom of a timeseries and removes the so-called tendancy from the timeseries (i.e. data)
def cubic_detrend(data):
    coef                        = np.polyfit(range(len(data)), data, 4)
    poly                        = np.polyval(coef, range(len(data)))
    data_detrended              = data - poly

    return data_detrended


# detrend_map: function that detrends a complete (time-lat-lon)-matrix with a cubic polynom
def detrend_map(matrix_3D):
    matrix_detrended        = np.copy(matrix_3D)

    for lat in range(np.size(matrix_3D,axis=1)):
        for lon in range(np.size(matrix_3D,axis=2)):
            matrix_detrended[:,lat,lon]      = cubic_detrend(matrix_3D[:,lat,lon])

    return matrix_detrended
