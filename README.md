## PROJECT: Does the absence of sea ice in the Arctic have an influence on the occurrence of extreme events over the Eastern part of Canada?
- SIMULATIONS: CanESM2-LE and ClimEx
- LANGUAGES: Python, Julia
- CONTACT: yann.chavaillaz@gmail.com
- DATE: 16th April 2019

## KEY STEPS
1. Clustering of years in the CanESM2-LE
2. Correspondence between CanESM2-LE and ClimEx simulations
3. Merging of the ClimEx files for one simulation and one season
4. Removal of the climate change trend in ClimEx simulations
5. Computation of seasonal and extreme indicators
6. Sorting of years into clusters
7. Mask of specific regions
8. Plotting of figures

Intermediate and final data, plus figures can be found on Neree in /exec/yanncha/sea_ice/.
Functions are defined in files ./functions_***.py
Climate variables: tasmin, tasmax, pr, prsn

## 1. Clustering of years in the CanESM2-LE
code: ./clustering/*
method: K-means clustering
input data: sea ice extent (sie - %) with a logarithmic transformation
3 clusters: no ice, ice, unclear
The temporal distribution of clusters can be represented in a histogram by the code ./histogram_clusters.py
The preparation of raw sie data to do the clustering is done with ./prepare_sic_september_forML.py

## 2. Correspondence between CanESM2-LE and ClimEx simulations
file of correspondance: /exec/yanncha/sea_ice/clusters/sic_september_clusters_kmeans_CanESM2-LE.npy

## 3. Merging of the ClimEx files for one simulation and one season
code: ./merge_months_[variable].py
need to specify: months and season (SON, DJFM, AMJ)
especially for pr: only hourly data is available. So first, transform hourly data to daily data with ./pr_hourlytodaily.py

## 4. Removal of the climate change trend in ClimEx simulations
code: ./detrend_[variable].py
need to specify: season
method: cubic polynomial fit

## 5. Computation of seasonal and extreme indicators
code: ./indices_[variable].py and ./residuals_[variable].py
need to specify: season
indicators for tasmin: minimum temperature of the season, 1st percentile, 5th percentile, seasonal average and season standard deviation
indicators for tasmax: maximum temperature of the season, 99th percentile, 95th percentile, seasonal average and season standard deviation
indicators for pr and prsn: daily maximum precipitation, 5-day maximum precipitation, seasonal average, seasonal standard deviation, relative sum of precipitation over the season

## 6. Sorting of years into clusters
code: ./sort_indices.py
need to specify: clim_var, indice, season
use of the correspondence of clusters between CanESM2-LE and ClimEx of step 2

## 7. Mask of specific regions
code: ./mask_adminQC.jl
shapefile: ./masking/admin_QC.[extension]
need to specify: regions_name, regions_code, regions_number

## 8. Plotting of figures
### a. Maps of difference between two clusters for three seasons
code: ./fig_deltamap_minmax.py
need to specify: var, indice, indice_name, extrema (min, max, mean of the distribution) and units (of the indice)
### b. PDF and qq-plot of different clusters for three seasons in Quebec
code: ./fig_distribution_qqplot.py
need to specify: var, indice, indice_name and units (of the indice)
### c. PDF and qq-plot of different clusters for three seasons in specific administrative regions of Quebec
code: ./fig_distribution_qqplot_regional.py
need to specify: var, indice, indice_name, units (of the indice) and scale (specific region defined in step 7)

## STILL TO BE DONE
Steps 6, 7 and 8 for prsn.
