# DMTCP Checkpointing Tutorial

Tutorial code for checkpointing SLURM jobs using DMTCP on Cheaha.

## Workflow Explanation

DMTCP is a state-based checkpointing system intended for single node tasks (MPI checkpointing is possible but in development, see: https://github.com/mpickpt/mana). A very simple explanation of its operation is that it records the state of the job (i.e. in-memory representation) to disk at a user-specified interval or on request to a coordinator. DMTCP waits until it can "break in" to the job's execution, pauses it, records its state, and then allows the job to resume.

The sample task contained here is a simple for-loop over a function which sleep for a random time and returns a random value. These values are formatted and printed to `stdout`. The loop is run 100 times for a median wait time of 0.5 seconds per iteration. Checkpoints are made every 5 seconds.

For more details on the specifics of each component of the execution, please see comments in each code file.

## Usage

Use the command `sbatch job.sh` to run the job. When the job is complete, try running `sbatch restart_job.sh`. You should see ` job.log` and `job-restart.log` files. Compare the last few lines of `job.log` and the contents of `job-restart.log`. They should be identical because the pseudo-random number generator state has been saved to disk as part of the checkpoint, leading to the precise repetition of the last part of the task.
