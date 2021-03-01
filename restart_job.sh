#!/bin/bash
#SBATCH --job-name=job-restart
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=express
#SBATCH --time=0:10:00
#SBATCH --output=%x.log
#SBATCH --error=%x.log

export DMTCP_COORD_HOST=localhost
module load DMTCP/2.5.0
module load Anaconda3
conda activate dmtcp-tutorial
./dmtcp_restart_script.sh
