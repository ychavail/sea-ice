#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kmeans_analysis.py:
Application of a Kmeans clustering on Arctic sea ice cover data.

Date of creation: 2018/05/03
Date of last modification: 2018/07/30

Authors: roy.philippe@ouranos.ca, chavaillaz.yann@ouranos.ca
"""

" loading packages "
import os
import numpy as np
import matplotlib.pyplot as plt
import functions_clustering as fct_cl
from functions_clustering import compare_rnd
from sklearn.cluster import KMeans
import sys

" preparing data for analysis "
file = '/exec/yanncha/sea_ice/sic_september_forML_CanESM2-LE.nc'
db, db_orig = fct_cl.loaddata(file)

" defining the clustering model to use and using it "
model = KMeans(n_clusters=3, random_state=0)
model.fit(db)

" ordering the clusters by years, families, members "
file_area       = '/exec/yanncha/area_data/areacella_CanESM2.nc'
area_seaice     = fct_cl.compute_totalsic(file_area,db_orig)

y       = np.arange(1950,2101)
years   = np.tile(y,50)

f       = np.arange(1,6)
f2      = np.tile(f,(151*10,1))
f3      = np.transpose(f2)
f4      = np.resize(f3,(1,np.size(f3)))
family  = f4[0]

m       = np.arange(1,11)
m2      = np.tile(m,(151,1))
m3      = np.transpose(m2)
m4      = np.resize(m3,(1,np.size(m3)))
member  = np.tile(m4[0],5)

mc      = np.array(['kda','kdb','kdc','kdd','kde','kdf','kdg','kdh','kdi','kdj',
'kdk','kdl','kdm','kdn','kdo','kdp','kdq','kdr','kds','kdt','kdu','kdv','kdw','kdx','kdy','kdz',
'kea','keb','kec','ked','kee','kef','keg','keh','kei','kej','kek','kel','kem','ken','keo','kep',
'keq','ker','kes','ket','keu','kev','kew','kex'])
mc2     = np.tile(mc,(151,1))
mc3     = np.transpose(mc2)
member_climex   = np.resize(mc3,np.size(mc3))

key_elements    = (family,member,member_climex,years,area_seaice,model.labels_)
clusters        = np.transpose(np.vstack(key_elements))


repfig = '/exec/yanncha/sea_ice/figures/fit/'
fct_cl.compare_rnd(model, db, repfig, 60)
np.save('/exec/yanncha/sea_ice/sic_september_clusters_kmeans_CanESM2-LE', clusters)
