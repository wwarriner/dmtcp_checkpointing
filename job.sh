#!/bin/bash
#SBATCH --job-name=job
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=express
#SBATCH --time=0:10:00
#SBATCH --output=%x.log
#SBATCH --error=%x.log

# Example of how to run a single-node DMTCP checkpointed task in SLURM on
# Cheaha.

# Load necessary modules for this example.
module load DMTCP/2.5.0
module load Anaconda3/2020.11

# To run this you will need to build the environment from env.yml. To do so
# please run: `conda env create --file env.yml`
conda activate dmtcp-tutorial

# Launches a dmtcp checkpointed task with example computations. The flag -i
# accepts a checkpoint interval in seconds. The python flag -u requests
# unbuffered streams, so logging is real-time. The value 100 is the number of
# steps to run in the loop in `task.py`.
dmtcp_launch -i 5 "python -u task.py 100"
