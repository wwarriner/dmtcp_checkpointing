"""
task.py

Written by William Warriner 2021
wwarr@uab.edu

Contains example process code which we want to checkpoint. The general workflow
is to loop through a sample computation which sleeps a random amount of time and
returns a random float. Both values are returned in a dict and printed to
stdout. This process is repeated
"""

import argparse
import random
import sys
import time
from typing import Dict

VALUE = "value"
SLEEP_TIME = "sleep_time"


def print_step(current_step: int, data: Dict[str, float]) -> None:
    """
    Prints the data dict containing the value and the sleep time, with an
    iteration count. We flush the buffer each time a line is printed to ensure
    real-time updating. We can (and do) use the `-u` argument, i.e. unbuffered
    streams, with the Python interpreter for the same effect.
    """
    print(
        f"Step {current_step+1: >4}: {data[VALUE]: >6.2f} ({data[SLEEP_TIME]: >6.2f}s)"
    )
    sys.stdout.flush()


def step() -> Dict[str, float]:
    """
    The kernel computation of interest which is run once per loop step. Computes
    a value using a lognormal distribution. Computes a sleep time using a
    triangular distribution to ensure non-negative values with a central
    tendency, and then sleeps for that amount of time. A dict is returned
    containing both.
    """
    value = random.lognormvariate(mu=0.0, sigma=1.0)
    sleep_time = abs(random.triangular(low=0.0, high=1, mode=0.5))
    time.sleep(sleep_time)
    return {VALUE: value, SLEEP_TIME: sleep_time}


def task(step_count: int) -> None:
    """
    The primary kernel loop. Runs the kernel `step()` function, then reports the
    values using `print_step()`. The only input is a positive integer which
    limits how many times the loop is executed.
    """
    assert 0 < step_count
    for current_step in range(step_count):
        data = step()
        print_step(current_step, data)


def interface() -> None:
    """
    The external interface. Prepares an argument parser accepting a positive
    integer steps. Steps is clipped to 100 for sanity.
    """
    parser = argparse.ArgumentParser(
        description="Run kernel function and report values. Intended for use as part of DMTCP checkpointing with SLURM tutorial on Cheaha."
    )
    parser.add_argument(
        "steps",
        metavar="N",
        nargs="?",
        default=100,
        type=_check_positive,
        help="positive integer number of steps to run, clipped to 100",
    )
    args = parser.parse_args()
    steps = args.steps[0]
    steps = min(steps, 100)
    task(steps)


def _check_positive(value: str) -> int:
    """
    Checks if a string supplied to argparse is a positive integer. Raises
    argparse.ArgumentTypeError if not.
    """
    try:
        ivalue = int(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"{value} must be an integer")
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} must be positive")
    return ivalue


if __name__ == "__main__":
    interface()
