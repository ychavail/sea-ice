#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
functions_clustering.py:
Functions useful for clustering Arctic sea ice maps.

Date of creation: 2018/05/03
Date of last modification: 2018/07/31

Authors: roy.philippe@ouranos.ca, chavaillaz.yann@ouranos.ca
"""

" loading packages "
import pandas as pd
import numpy as np
import netCDF4 as netcdf
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import QuantileTransformer
from scipy.stats import boxcox
from scipy.special import inv_boxcox
from sklearn.model_selection import train_test_split


" logtransform(database): applying a logarithmic transformation to a database "
def logtransform(db):
    dbout = np.log(db + 10)

    return dbout

" loaddata(file): loading sea ice cover data from a netcdf file, defining a dataframe, and preparing data for cluster analysis "
def loaddata(file=''):

    nc              = netcdf.Dataset(file,'r')
    data_nc         = nc.variables['sic'][:,:]
    df              = pd.DataFrame(data=data_nc)
    df_orig         = df

    # logarithmic transformation
    df2 = logtransform(df)

    # standard scaler
    preproStandard = StandardScaler()
    preMinMax = MinMaxScaler()
    preRobust = RobustScaler()
    preQuantile = QuantileTransformer()

    # fit standard scaler (only on train data to avoid bias)
    #preproStandard.fit(df)
    #preMinMax.fit(df)
    #preRobust.fit(df)
    preQuantile.fit(df2)

    # apply scaler to Train and Test
    #df_standard = preproStandard.transform(df)
    #df_minmax = preMinMax.transform(df)
    #df_robust = preRobust.transform(df)
    df_quantile = preQuantile.transform(df2)

    return df_quantile, df_orig

" computing the total sea ice cover in the Arctic "
def compute_totalsic(file_area,db):

    nc          = netcdf.Dataset(file_area,'r')
    areacella   = nc.variables['areacella'][51:,:]
    area_rs     = np.resize(areacella,(1,np.size(db,1)))
    sic_area    = area_rs*db
    sic_tot     = np.sum(sic_area,axis=1)/1000000
    sic_tot[sic_tot<10] = 0

    return sic_tot


def compare_rnd(model, db, repfig, nb):

    # Random index
    idxrnd = np.random.randint(0, len(model.labels_), nb)

    for idx in idxrnd:
        img = db[idx, :].reshape(13, 128)
        plt.figure()
        plt.pcolormesh(img)
        plt.title(model.labels_[idx])
        filename = repfig + str(idx) + '.png'
        plt.savefig(filename)
        plt.close()
