#!/bin/bash
#SBATCH --job-name=job
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=express
#SBATCH --time=0:10:00
#SBATCH --output=%x.log
#SBATCH --error=%x.log

module load DMTCP/2.5.0
module load Anaconda3
conda activate dmtcp-tutorial
dmtcp_launch -i 5 "python -u task.py 100" # -u means unbuffered, we get logging in real-time
