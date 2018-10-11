import xarray as xr
import glob

from multiprocessing import Pool

def main():
    MRCC5 = {}


    MRCC5['CanESM2_r1i1p1'] = {}
    MRCC5['CanESM2_r1i1p1']['hist'] = 'bby'
    MRCC5['CanESM2_r1i1p1']['rcp85'] = 'bbz'
    MRCC5['CanESM2_r1i1p1']['rcp45'] = 'bca'

    MRCC5['CNRM-CM5_r1i1p1'] = {}
    MRCC5['CNRM-CM5_r1i1p1']['hist'] = 'bcc'
    MRCC5['CNRM-CM5_r1i1p1']['rcp85'] = 'bcd'
    MRCC5['CNRM-CM5_r1i1p1']['rcp45'] = 'bce'

    MRCC5['MPI-ESM-LR_r1i1p1'] = {}
    MRCC5['MPI-ESM-LR_r1i1p1']['hist'] = 'bcg'
    MRCC5['MPI-ESM-LR_r1i1p1']['rcp85'] = 'bch'
    MRCC5['MPI-ESM-LR_r1i1p1']['rcp45'] = 'bcw'

    MRCC5['GFDL-ESM2M_r1i1p1'] = {}
    MRCC5['GFDL-ESM2M_r1i1p1']['hist'] = 'bcj'
    MRCC5['GFDL-ESM2M_r1i1p1']['rcp85'] = 'bck'
    MRCC5['GFDL-ESM2M_r1i1p1']['rcp45'] = 'bcr'

    root = r'W:/ClimateData/'
    vari = ['pr','tas','uas','vas','rlds','rsds','ps','huss']

    paths = {'dmf2','expl6','expl7'}

    latBnds = [43,50]
    lonBnds = [-67,-80]
    outrep = 'H:/TRAVIS_Foret/PROJETS/ForetSadapter/ClimateData/AudreyMaheu'
    sims = MRCC5.keys()

    for s in sims:
        rcps = MRCC5[s].keys()
        for r in rcps:
            if 'hist' in r:
                years = range(1951,2006)
            else:
                years = range(2006,2101)
            s_id = MRCC5[s][r]
            for v in vari:
                for p in paths:
                    for y in years:
                        for m in range(1,13):
                            inrep = str(y)+str(m).zfill(2)
                            list1 = glob.glob(root + p + '/climato/arch/' + s_id + '/series/' + inrep + '/*' + v + '_' + '*.nc')



                            for l in list1:
                                outrep1 = outrep + '/' + 'MRCC5-' + s + '/' + r + '/' + v
                                subset_nc(l,latBnds,lonBnds,outrep1)



def subset_nc(ncfile,latBnds,lonBnds,outrep):
    if not glob.os.path.exists(outrep):
        glob.os.makedirs(outrep)
    outfile = outrep + '/' + ncfile.split('/')[-1].split('\\')[-1].replace('.nc','_subset.nc')


    ds = xr.open_dataset(ncfile,decode_times=False)

    dsSub = ds.where((ds.lon>min(lonBnds))&(ds.lon<max(lonBnds))&(ds.lat>min(latBnds))&(ds.lat<max(latBnds)),drop=True)
    comp = dict(zlib=True, complevel=5)
    encoding = {var: comp for var in ds.data_vars}
    dsSub.to_netcdf(outfile,format='NETCDF4',encoding=encoding)

if __name__ == '__main__':
    main()
