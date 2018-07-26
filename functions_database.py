##################################################################
# Description: Tools to fetch into a database of netcdf files containing CanESM2-LE or ClimEx data.
# Code name: functions_database.py
# Date of creation: 2018/03/26
# Date of last modification: 2018/03/26
# Contacts: chavaillaz.yann@ouranos.ca
##################################################################

## Needed packages
import os
import numpy as np
import fnmatch
import netCDF4 as netcdf


# ncdbsearch: function that searches recursively in a path (datadir) to generate a database (dictionary) of simulations stored as nc files archived in a CMIP-like structure
def ncdbsearch(datadir,scenarios=[],realms=[],tres=[],variables=[],models=[],members=[]):

    # creation of a list of paths where all CMIP5 data is
    paths=findncfiles(datadir)
      
    # selection of simulations according to all criterias in the given path
    if len(scenarios)>0:
        paths=[paths[i] for i in np.arange(len(paths)) for kw in scenarios
               if '_'+kw.lower()+'_' in paths[i].lower()]
    if len(realms)>0:
        paths=[paths[i] for i in np.arange(len(paths)) for kw in realms
               if '_'+kw.lower()+'_' in paths[i].lower()]
    if len(tres)>0:
        paths=[paths[i] for i in np.arange(len(paths)) for kw in tres
               if '_'+kw.lower()+'_' in paths[i].lower()]                
    if len(models)>0:
        paths=[paths[i] for i in np.arange(len(paths)) for kw in models
               if '_'+kw.lower()+'_' in paths[i].lower()]
    if len(variables)>0:
        paths=[paths[i] for i in np.arange(len(paths)) for kw in variables
               if '/'+kw.lower()+'_' in paths[i].lower()]
    if len(members)>0:
        paths=[paths[i] for i in np.arange(len(paths)) for kw in members
               if '_'+kw.lower() in paths[i].lower()]
    
    paths.sort()	# arrange paths in alphabetic order
    i=0 		# counter 
    simdb=[] 		# initialization of the database of selected simulations
    
    # creation of the database
    for path in paths:
        pathpre=datadir
        pathsuf=path.split(datadir)[1]
        var,mod,scen,mem,tstamp=cmip5filestrinfo(pathsuf)
        simdb.append({'id':i,'mod':mod,'scen':scen,'var':var,'mem':mem,'pathpre':pathpre,'pathsuf':pathsuf})
        i+=1
    
    # if useful at this stage: calling the nice function to print in a convienient way the database in your terminal
    #printdb(simdb)

    # store the database in simdb
    return simdb
###


# printdb: this is just a nice display of the ncdbsearch output in a terminal
def printdb(simdb):

    print()
    print("%3s %14s %10s %7s %8s %60s" % ('id','mod','scen','var','mem','file'))
    print('----------------------------------------------------------------------------------------------------------------')
    for entry in simdb:
        print("%3s %17s %10s %7s %8s %60s" % (entry['id'],entry['mod'],entry['scen'],entry['var'],entry['mem'],os.path.basename(entry['pathsuf'])))
###


# findncfiles: recursively find all netcdf files in a specific path
def findncfiles(path,fstrmatch=''):

	fstrmatch=fstrmatch+'*.nc'
	matches = []
	for root, dirnames, filenames in os.walk(path):
		for filename in fnmatch.filter(filenames, fstrmatch):
			try:
				with netcdf.Dataset(os.path.join(root,filename)) as f:
					pass
			except:
				continue
			matches.append(os.path.join(root, filename))
	return matches
###


# simdbrejecttslice: filter a simdb (i.e. an output from the ncdbsearch function) by rejecting a time slice beginning at yyyymm (for monthly data), yyyymmdd (for daily data), yyyyddmmhh (for 6hr data) or later. Can be useful for RCP scenarios when you just want to select 21st-century-simulations and not later
def simdbrejecttslice(simdb,yyyymm):
    
    simdbnew=[]		# initialization of a new database of simulations
    for ii in range(len(simdb)):
	# check if each file begins at or after yyyymm by looking at the file name
        if int(simdb[ii]['pathsuf'].split('/')[-1].split('_')[-1].split('-')[0]) < yyyymm:
            simdbnew.append(simdb[ii])
   
    # calling the nice function to print in a convienient way the database in your terminal 
    #printdb(simdbnew)

    # store the new database in simbdnew    
    return simdbnew
###


# simdbrejecttslice2: filter a simdb (i.e. an output from the ncdbsearch function) by rejecting a time slice ending at yyyymm (for monthly data), yyyymmdd (for daily data), yyyyddmmhh (for 6hr data) or later. Can be useful for historical scenarios when you just want to select the end of the historical period and not sooner
def simdbrejecttslice2(simdb,yyyymm):
    
    simdbnew=[]		# initialization of a new database of simulations
    for ii in range(len(simdb)):
	# check if each file begins at or after yyyymm by looking at the file name
        if int(simdb[ii]['pathsuf'].split('/')[-1].split('_')[-1].split('-')[-1].split('.')[0]) > yyyymm:
            simdbnew.append(simdb[ii])
   
    # calling the nice function to print in a convienient way the database in your terminal 
    #printdb(simdbnew)

    # store the new database in simbdnew    
    return simdbnew
###

# simdbrejectduplication: filter a simdb (i.e. an output from the ncdbsearch function) by rejecting duplication of data. Can be useful for additional (useless) CMIP5 files at the end of the historical period.
def simdbrejectduplication(simdb):

	simdbnew	= []	
	simdbnew.append(simdb[0])	# initialization of a new database of simulations
	minus		= 0 
	for ii in range(1,len(simdb)):
		# check if each file has not common data with the previous one
		if (simdb[ii]['mod'] == simdb[ii-1]['mod']) and (simdb[ii]['mem'] == simdb[ii-1]['mem']) and (simdb[ii]['scen'] == simdb[ii-1]['scen']) and (simdb[ii]['pathsuf'].split('/')[-1].split('_')[-1].split('-')[-1] == simdb[ii-1]['pathsuf'].split('/')[-1].split('_')[-1].split('-')[-1]) and (simdb[ii]['pathsuf'].split('/')[-1].split('_')[-1].split('-')[0] >= simdb[ii-1]['pathsuf'].split('/')[-1].split('_')[-1].split('-')[0]):
			minus			= minus + 1
		else:
			simdbnew.append(simdb[ii])
			simdbnew[-1]['id']	= simdbnew[-1]['id'] - minus
	
	return simdbnew
### 


# simdbintersection: from simdb's of two different climate variables (i.e. an output from the ncdbsearch function), remove all the simulations that are not in common in the two databases
def simdbintersection(simdb1,simdb2):
	simdbnew_1 = []
	simdbnew_2 = []
	for i1 in simdb1:
		for i2 in simdb2:
			if (i1['mod']==i2['mod']) and (i1['mem']==i2['mem']) and (i1['scen']==i2['scen']):
				if i1 not in simdbnew_1:
                			simdbnew_1.append(i1)
				if i2 not in simdbnew_2:
                			simdbnew_2.append(i2)
	ind1 = 0
	ind2 = 0
	for i1 in simdbnew_1:
		i1['id'] = ind1
		ind1 = ind1 + 1
	for i2 in simdbnew_2:
		i2['id'] = ind2
		ind2 = ind2 + 1

	# calling the nice function to print in a convienient way the database in your terminal 
	#printdb(simdbnew_1)
	#printdb(simdbnew_2)
	
	return simdbnew_1,simdbnew_2
###


# simdbgetlist: from a simdb (i.e. an output from the ncdbsearch function), get the exact list of simulations included, indeed a simulation can be split (in time) in several files
def simdbgetlist(simdb): 
	l = [[simdb[0]['mod'],simdb[0]['mem']]]
	for i in simdb:
        	if (i['mod']!=l[-1][0]) or (i['mem']!=l[-1][1]):
                	l.append([i['mod'],i['mem']])
	
	return l
###


# cmip5filestrinfo: extract info from nc file name in the CMIP5 format such as: tas_Amon_MIROC-ESM_1pctCO2_r1i1p1_000101-014012.nc Can be given as a path but only basename is considered. Use: var,mod,scen,mem,tstamp=cmip5filestringinfo(string)
def cmip5filestrinfo(string):

    fname=os.path.basename(string)
    try:
        var,tmp,mod,scen,mem,tstamp=fname.split('.')[0].split('_')
    except:
        var,tmp,mod,scen,mem=fname.split('.')[0].split('_')
        tstamp='???'
    
    return var,mod,scen,mem,tstamp

###
