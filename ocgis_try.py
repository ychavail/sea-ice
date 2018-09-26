

import os

import ocgis
from ocgis import OcgOperations, RequestDataset, env
from ocgis.test.base import create_gridxy_global, create_exact_field

import functions_detrending as fct_d

simulation = 'kda'
variable = 'tasmax'
months = ('06', '07','08')

paths = fct_d.select_months(simulation, months)
filepaths = []

for p in paths:
    time = p[-6:]
    filepaths.append(os.path.join(p, '{0}_­{1}_{2}_se.nc'.format(variable, simulation, time)))

print(filepaths)

# This is where to find the shapfiles.
#ocgis.env.DIR_GEOMCABINET = os.path.join(os.getcwd(), os.path.split(ocgis.test.__file__)[0], 'bin')




#ops = OcgOperations(dataset=rds, spatial_operation='clip', aggregate=True, snippet=SNIPPET, geom='state_boundaries', geom_select_uid=[16])
#ret = ops.execute()
#ops = OcgOperations(dataset=rds, spatial_operation='clip', aggregate=True, snippet=SNIPPET, geom='state_boundaries')
#ret = ops.execute()
#assert len(ret.geoms) == 51
