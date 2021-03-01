#!/bin/bash
#SBATCH --job-name=job-restart
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=express
#SBATCH --time=0:10:00
#SBATCH --output=%x.log
#SBATCH --error=%x.log

# Example of how to restart a DMTCP checkpointed task in SLURM on Cheaha.

# Load necessary modules for this example.
module load DMTCP/2.5.0
module load Anaconda3

# Activate the environment.
conda activate dmtcp-tutorial

# This export is required because, by default, DMTCP records the actual hostnome
# of the node it runs on. On Cheaha, this will be something like `c0038`, and it
# isn't guaranteed you will be able to get back on that same node. Setting the
# DMTCP host to `localhost` ensures the script will run on whatever node the
# restart job ends up on.
export DMTCP_COORD_HOST=localhost

# The script below is created automatically as part of the checkpointing
# process.
./dmtcp_restart_script.sh
