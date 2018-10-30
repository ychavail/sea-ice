##################################################################
# Description: Functions enabling to sort the matrix of an indice by clusters.
# Code name: functions_sorting.py
# Date of creation: 2018/10/24
# Date of last modification: 2018/10/24
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import numpy as np
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
