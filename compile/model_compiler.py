"""Compiles different models by changing up the ML model inside the ../mbed file
that contains our mbed project. Will copy all of the finished systems to a different
folder."""
import subprocess
from subprocess import run
from subprocess import check_output
from pathlib import Path
import shutil as sh

PROG_PATH = Path.cwd().parent / "mbed"
MODEL_FILE_PATH = PROG_PATH / "tensorflow" / "lite" / "micro" / "examples" / "hello_world"
MODEL_FILE_NAME = "tinyml_model_data.h"
OUTPUT_MODEL_FOLDER = Path.cwd() / "mbed_models"


def get_avaiable_programs():
    """Gets the available model names that can be loaded into our program.
    All of the available models should be in the file path
        mbed/tensorflow/lite/micro/examples/hello_world/tinyml_model_data.h
        mbed/tensorflow/lite/micro/examples/hello_world/tinyml_model_data.cc
    """
    # scrape out all lines in that program that have [], which are the model
    # binary definitions.
    text = (MODEL_FILE_PATH / MODEL_FILE_NAME).read_text()
    replacement_list = ['extern', 'unsigned', 'char', '[', ']', ';']
    model_names = []
    for line in text.split('\n'):
        if '[' in line:
            for remove in replacement_list:
                line = line.replace(remove, "")
            var = line.strip()
            model_names.append(var)
    return model_names

def compile_program(model_name, debug=True):
    """Actually calls mbed to compile programs, then copy out the binary
    The binary will be in the format:
        ./BUILD/<DEVICE_NAME>/GCC_ARM/mbed.bin
    """
    command = "mbed compile -t GCC_ARM -DTF_LITE_STATIC_MEMORY"
    command += f" -DTINYML_MODEL={model_name}"
    if debug:
        command += " -DTINYML_DEBUG"
    # command += " -DARM_MATH_LOOPUNROLL"
    print(command)
    p = check_output(command, shell=True, cwd=PROG_PATH)

    # Get the image location from the output
    image_path = None
    for line in p.decode().split('\n'):
        if "Image:" in line:
            image_path = line.split(' ')[-1]
            break
    if image_path is None:
        print("Could not find the image file for some reason. Skipping.")
        return
    

    binary_path = PROG_PATH / image_path
    device_name = binary_path.parent.parent.stem
    output_model_path = OUTPUT_MODEL_FOLDER / device_name / (model_name + ".bin")
    if not output_model_path.parent.is_dir():
        output_model_path.parent.mkdir(exist_ok=True, parents=True)
    print(f"mv {binary_path} {output_model_path}")
    
    sh.move(binary_path, output_model_path)



if __name__ == '__main__':
    model_names = get_avaiable_programs()
    num_models = len(model_names)
    print(f"Found {num_models} models to be compiled.")
    
    for idx, model_name in enumerate(model_names):
        print(f"[{idx}/{num_models}]")
        compile_program(model_name)