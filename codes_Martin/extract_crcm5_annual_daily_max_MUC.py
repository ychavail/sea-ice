import numpy as np
import climex_utils as cu
import matplotlib.pyplot as plt
import rcm as rcm
import sys
reload(cu)


try:
    __IPYTHON__

    run1=0
    run2=9
    domain='QC'

except:
    print sys.argv, len(sys.argv)
    if len(sys.argv)==4:
        run1=int(sys.argv[1])
        run2=int(sys.argv[2])
        domain=sys.argv[3]
    else:
        sys.exit('Wrong number of arguments: variable season')        


y1,y2=2000,2019
sea='ANN'
vv='pr'

years=np.arange(y1,y2+1)

if domain=='QC':
    runs=cu.climex_qc_runs[run1:run2+1]
elif domain=='EU':
    runs=cu.climex_eu_runs[run1:run2+1]

print runs

dailyAMPstack=[]
for run in runs:
    for year in years:
        yyyymms=cu.get_labels_yyyymms_from_season_years(sea,[year])
        #data,tts=cu.append_series_from_yyyymms(run,vv,yyyymms,wtime=1,gp=[100,100])
        data,tts=cu.append_series_from_yyyymms(run,vv,yyyymms,wtime=1)

        blocksize=24

        if len(tts) % blocksize != 0:
            sys.exit('Blocksize error.')

        data_sums=[]
        kk=1
        dsum=0
        zz=1
        for ii in range(len(tts)):
            if kk<=blocksize:
                dsum+=data[ii]
                if kk==blocksize:
                    data_sums.append(dsum)
                    kk=1
                    dsum=0
                    zz+=1
                    continue
                kk+=1

        data_sums=np.array(data_sums)

        dailyAMP=np.max(data_sums,axis=0)

        dailyAMPstack.append(dailyAMP)
    
dailyAMPstack=np.array(dailyAMPstack)

# Save data
npdir_save='/gpfs/work/pr94lu/di73tat/Analysis/npy-files-extremes/'
np_file='_'.join(['AMP','THREADS',domain,vv,sea,runs[0]+'-'+runs[-1],str(y1)+'-'+str(y2)])
np.save(npdir_save+np_file,dailyAMPstack)



# lat,lon = cu.get_latlon_from_domain('QC')
# rcm.plotrcm(dailyAMP,lon,lat,clevs=10,units='',tight=1)


# Find days
# day0=datetime.datetime(tts[0].year,tts[0].month,tts[0].day)
# daysid=[0]
# days={}
# days_list=[day0]
# days[day0]=[]

# for kk,tt in enumerate(tts[1:]):
#     if datetime.datetime(tt.year,tt.month,tt.day) == day0:
#         daysid.append(kk)
#     else:
#         days_list.append(day0)
#         days[day0]=daysid

#         daysid=[]
#         day0=datetime.datetime(tt.year,tt.month,tt.day)

# days[day0]=daysid

# daysid=[]
# day0=datetime.datetime(tt.year,tt.month,tt.day)        
    
