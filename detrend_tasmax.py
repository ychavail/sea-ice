##################################################################
# Description: Code selecting all the files from the ClimEx ensemble
# for a specific climate variable and specific months, masking the
# data over the Quebec province, detrending the climate change component
# saving a new netcdf-file for each of the 50 ClimEx simulations.
# Code name: detrend_tasmax.py
# Date of creation: 2018/10/04
# Date of last modification: 2018/10/04
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

# Needed packages
import os
import ocgis
from ocgis import OcgOperations, RequestDataset, env
from ocgis.test.base import create_gridxy_global, create_exact_field
import functions_detrending as fct_d
import sys


# Initialization
#simulations = ["kda","kdb","kdc","kdd","kde","kdf","kdg","kdh","kdi","kdj","kdk",
#"kdl","kdm","kdn","kdo","kdp","kdq","kdr","kds","kdt","kdu","kdv","kdw","kdx",
#"kdy","kdz","kea","keb","kec","ked","kee","kef","keg","keh","kei","kej","kek",
#"kel","kem","ken","keo","kep","keq","ker","kes","ket","keu","kev","kew","kex"]
simulations = ["kda"]
var = "tasmax"
var_nc = ["tasmax"]
months = ("06","07","08")

### LOOP ON SIMULATIONS
for sim in simulations:

    # Selection of the paths and filenames corresponding to our criteria
    paths = fct_d.select_months(sim, months)
    filepaths = []
    for p in paths:
        month = p[-6:]
        filepaths.append(os.path.join(p, "{0}_{1}_{2}_se.nc".format(var, sim, month)))
    filenames   = []
    for p in filepaths:
        f = os.path.split(p)[-1].split('.')[0]
        filenames.append(f)


    # Mask over the Quebec province
    ## Return all time slices
    #SNIPPET = True
    ## Data returns won't overwrite in this case.
    #env.OVERWRITE = False

    ## where to find the shapefiles
    #ocgis.env.DIR_GEOMCABINET = os.path.join(os.getcwd(), os.path.split(ocgis.test.__file__)[0], 'bin')
    #ocgis.env.DIR_GEOMCABINET = os.path.join(os.getcwd(), "shapefiles")

    #rds = [RequestDataset(uri=uri, variable=variable ,field_name=field_name) for uri, var, field_name in zip(filepaths, filenames, var_nc)]
#ops = OcgOperations(dataset=rds, spatial_operation='clip', aggregate=True, snippet=SNIPPET, geom='prov_la_p_geo83_f', geom_select_uid=[1])
#ret = ops.execute()

    #assert len(ret.geoms) == 51


    # Removing the climate change tendancy from the data
    # initialization of the data... (netcdf or product of the mask?)
    for p in filepaths:
        # question: dans quel ordre faire les boucles? Demander à Philippe. Fichier, lat, lon?
