from subprocess import run
from subprocess import TimeoutExpired
from subprocess import CalledProcessError
from pathlib import Path
import argparse
import os
import time


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
    run(command, shell=True)
    time.sleep(copy_time)

    # Actually reset the MCU, and read the output it generates. We timeout after
    # <bench_time> seconds since theoretically our MCU sould look forever.
    try:
        command = f"mbed sterm -r >> {output_path}"
        print(command)
        run(command, shell=True, check=True, timeout=bench_time)
    except TimeoutExpired:
        pass
    except CalledProcessError:
        print("Error with mbed sterm command, not our usual timeout.")


if __name__ == '__main__':
    device = get_attached_devices()
    binary_models = list((BINARY_FOLDER / TESTING_DEVICE).glob("*"))
    print(f"Found {len(binary_models)} to benchmark.")
    print(f"Using device {device} for benchmarking.")

    