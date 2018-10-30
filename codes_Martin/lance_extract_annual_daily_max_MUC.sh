#!/bin/sh
#@ job_type = MPICH
#@ class = micro
#@ island_count=1,1
#@ node = 4
#@ total_tasks=20
#@ wall_clock_limit = 48:00:00
#@ job_name = lance_extract_annual_daily_max_MUC
#@ initialdir = /home/hpc/pr94lu/di73tat/listings/small_jobs
#@ output = $(job_name)_$(jobid).out
#@ error =  $(job_name)_$(jobid).err
#@ queue
set -eax


. /etc/profile.d/modules.sh
module rm mpi.ibm
module load python/2.7_anaconda_mpi

PYTHONPATH="/home/hpc/pr94lu/di73tat/python/climate-common:/home/hpc/pr94lu/di73tat/python/climex-analysis:/home/hpc/pr94lu/di73tat/python-lib/lib/python:/home/hpc/pr94lu/di73tat/OURALIB/V1.4.0dev/lib/python:${PYTHONPATH}"


python extract_crcm5_annual_daily_max_MUC.py 0   4 QC &
python extract_crcm5_annual_daily_max_MUC.py 5   9 QC &
python extract_crcm5_annual_daily_max_MUC.py 10 14 QC &
python extract_crcm5_annual_daily_max_MUC.py 15 19 QC &
python extract_crcm5_annual_daily_max_MUC.py 20 24 QC &
python extract_crcm5_annual_daily_max_MUC.py 25 29 QC &
python extract_crcm5_annual_daily_max_MUC.py 30 34 QC &
python extract_crcm5_annual_daily_max_MUC.py 35 39 QC &
python extract_crcm5_annual_daily_max_MUC.py 40 44 QC &
python extract_crcm5_annual_daily_max_MUC.py 45 49 QC &

python extract_crcm5_annual_daily_max_MUC.py 0   4 EU &
python extract_crcm5_annual_daily_max_MUC.py 5   9 EU &
python extract_crcm5_annual_daily_max_MUC.py 10 14 EU &
python extract_crcm5_annual_daily_max_MUC.py 15 19 EU &
python extract_crcm5_annual_daily_max_MUC.py 20 24 EU &
python extract_crcm5_annual_daily_max_MUC.py 25 29 EU &
python extract_crcm5_annual_daily_max_MUC.py 30 34 EU &
python extract_crcm5_annual_daily_max_MUC.py 35 39 EU &
python extract_crcm5_annual_daily_max_MUC.py 40 44 EU &
python extract_crcm5_annual_daily_max_MUC.py 45 49 EU &

wait
echo "Script termine normalement"



