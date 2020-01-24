from subprocess import run
from subprocess import TimeoutExpired
from subprocess import CalledProcessError
from pathlib import Path
import argparse
import os
import time
import shutil as sh
import random


BINARY_FOLDER = Path.cwd() / 'mbed_models'
TESTING_DEVICE = 'NUCLEO_F767ZI'
OUTPUT_FOLDER = Path.cwd() / 'mbed_results'

def get_attached_devices():
    """Gets the mounted MCUs. Will return the first one by default.
    Please only have the MCU being tested. Needs to be modified for MAC
    TODO: Modify to work on mac."""
    BASE_DIR = Path("/media") / Path.home().stem
    devices = list(BASE_DIR.glob("*"))
    print(f"Found devices: {devices}, will use the first one.")
    return devices[0]


def run_binary(binary_path, device, output_path, copy_time=10, bench_time=10):
    """Takes in a path to a binary and deploys it onto our MCU.
    Make sure that this binary actually corresponds to the device you are
    benchmarking on!"""
    # Unfortunately the CP command doesn't actually block, so we just
    # wait a little bit of time for the model to flash
    command = f"cp {binary_path} {device}"
    print(command)
    fail_counter = 0
    while True:
        try:
            sh.copy(binary_path, device)
            break
        except OSError:
            fail_counter += 1
            if fail_counter > 5:
                print("Failed 5 times, stopping... Maybe replug the MCU?")
                exit(1)
    time.sleep(copy_time)

    # Actually reset the MCU, and read the output it generates. We timeout after
    # <bench_time> seconds since theoretically our MCU sould look forever.
    try:
        command = f"mbed sterm -r >> {output_path}"
        run(['mbed', 'sterm', '--reset'], timeout=bench_time)
    except TimeoutExpired:
        pass
    except CalledProcessError:
        print("Error with mbed sterm command, not our usual timeout.")


if __name__ == '__main__':
    device = get_attached_devices()
    binary_models = list((BINARY_FOLDER / TESTING_DEVICE).glob("*"))
    num_models = len(binary_models)
    output_logs = OUTPUT_FOLDER / f"{TESTING_DEVICE}.log"
    print(f"Found {num_models} to benchmark.")
    print(f"Using device {device} for benchmarking.")

    random.shuffle(binary_models)
    for idx, binary_model in enumerate(binary_models):
        print(f"[{idx}/{num_models}]")
        run_binary(binary_model, device, output_logs)

        