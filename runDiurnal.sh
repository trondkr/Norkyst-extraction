#!/bin/bash
#
#  Give the job a name
#PBS -N "norkystExtract"
#
#  Specify the project the job belongs to
#PBS -A nn9297k
#PBS -q normal
#PBS -l mppwidth=1,walltime=12:00:00
#PBS -l mppmem=2000MB
#PBS -l mppnppn=16
#
#  Send me an email on  a=abort, b=begin, e=end
#PBS -m abe
#
#  Use this email address (check that it is correct):
#PBS -M trond.kristiansen@niva.no
#
#  Write the standard output of the job to file 'mpijob.out' (optional)
#PBS -o  diurnal.out
#
#  Write the standard error of the job to file 'mpijob.err' (optional)
#PBS -e  diurnal.err
#

#  Make sure I am in the correct directory
cd /work/shared/nn9297k/Norkyst
module load python

export MPLCONFIGDIR=${pwd}
export TMP=`pwd`
export PYTHON_EGG_CACHE=/work/shared/nn9297k/Norkyst

aprun -B python calculateDiurnalAnomalies.py > diurnal.log