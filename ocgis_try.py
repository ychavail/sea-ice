##################################################################
# Description:
# Code name:
# Date of creation: 2018/10/04
# Date of last modification: 2018/10/04
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

import os

import ocgis
from ocgis import OcgOperations, RequestDataset, env
from ocgis.test.base import create_gridxy_global, create_exact_field
import sys

import functions_detrending as fct_d

simulation = "kda" # il faudra faire ensuite une boucle sur les simulations ClimEx
variable = "tasmax"
var_nc = ["tasmax"]
months = ("06","07","08")

paths = fct_d.select_months(simulation, months)
filepaths = []

for p in paths:
    month = p[-6:]
    filepaths.append(os.path.join(p, "{0}_{1}_{2}_se.nc".format(variable, simulation, month)))

filenames   = []
for p in filepaths:
    f = os.path.split(p)[-1].split('.')[0]
    filenames.append(f)

# Return all time slices
SNIPPET = True
# Data returns won't overwrite in this case.
env.OVERWRITE = False

# where to find the shapefiles
#ocgis.env.DIR_GEOMCABINET = os.path.join(os.getcwd(), os.path.split(ocgis.test.__file__)[0], 'bin')
ocgis.env.DIR_GEOMCABINET = os.path.join(os.getcwd(), "shapefiles")

rds = [RequestDataset(uri=uri, variable=variable ,field_name=field_name) for uri, var, field_name in zip(filepaths, filenames, var_nc)]
ops = OcgOperations(dataset=rds, spatial_operation='clip', aggregate=True, snippet=SNIPPET, geom='prov_la_p_geo83_f', geom_select_uid=[1])
ret = ops.execute()

#assert len(ret.geoms) == 51
