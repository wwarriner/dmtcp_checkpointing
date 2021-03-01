from typing import Dict
import argparse
import random
import time
from mpi4py import MPI
import sys

VALUE = "value"
WAIT = "wait"


def print_step(current_step: int, data: Dict[str, float]):
    print(f"Step {current_step+1: >4}: {data[VALUE]: >6.2f} ({data[WAIT]: >6.2f}s)")
    sys.stdout.flush()


def step() -> Dict[str, float]:
    value = random.lognormvariate(mu=0.0, sigma=1.0)
    wait = abs(random.triangular(low=0.0, high=1, mode=0.5))
    time.sleep(wait)
    return {VALUE: value, WAIT: wait}


def task(step_count: int) -> None:
    for current_step in range(step_count):
        data = step()
        print_step(current_step, data)


def task_mpi(step_count: int) -> None:
    # TODO import trace
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print_rank = size
    compute_size = size - 1
    DATA_TAG = 1

    for current_step in range(step_count):
        print(f"rank: {rank}, step: {current_step}")
        if rank == print_rank:
            print(f"rank: {rank}, receiving...")
            req = comm.irecv(source=comm.MPI_ANY_SOURCE, tag=DATA_TAG)
            print(f"rank: {rank}, waiting for recv...")
            data = req.wait()
            print(f"rank: {rank}, received!")
            print_step(**data)
        else:
            if current_step % compute_size != rank:
                continue
            print(f"rank: {rank}, computing...")
            data = step()
            print(f"rank: {rank}, sending...")
            req = comm.isend(
                {"current_step": current_step, "data": data}, dest=0, tag=DATA_TAG
            )
            print(f"rank: {rank}, waiting for send...")
            req.wait()
            print(f"rank: {rank}, sent!")


def interface() -> None:
    parser = argparse.ArgumentParser(description="Run steps.")
    parser.add_argument(
        "steps", metavar="N", nargs=1, type=int, help="number of steps to run"
    )
    parser.add_argument("--mpi", metavar="m", action="store_true", help="use mpi?")
    args = parser.parse_args()
    task(args.steps[0])


if __name__ == "__main__":
    interface()
