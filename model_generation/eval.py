"""A python version of the training script. Goes through a few parameters
and places all of the training models into individual folders."""
from subprocess import check_output
import subprocess
from pathlib import Path

# Make sure you clone tensorflow's original repository
# as well as their model repository. Clone the models repo
# underneath the original base tensorflow directory.
# git clone http://www.github.com/tensorflow/tensorflow
# git clone http://www.github.com/tensorflow/models
# then add your links to where those libraries are.
# seems to work best with tensorflow version 1.15
# or else the contrib modules are not installed by default
#
# Take a look at this link
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/micro/examples/person_detection/training_a_model.md


# Paths to the actual data as well as the tensorflow source directory.
TF_SOURCE = Path.home() / 'packages' / 'tensorflow'
VWW_DATASET = TF_SOURCE / 'models' / 'research' / 'slim' / 'mscoco'
MODEL_DIR = Path.cwd() / 'models'
LOGFILE = Path.cwd() / 'eval.log'


# Model parameters that we would like to use.
PREPROCESSING_NAME = 'mobilenet_v1'  # method of preprocessing training data
TRAIN_IMAGE_SIZE = 96


model_folders = list(MODEL_DIR.glob("*"))
num_models = len(model_folders)
print(f"Found {num_models} models to evaluate.")


result_dict = {}
with LOGFILE.open('w') as log_file:
    for model_folder in model_folders:
        model_name = model_folder.stem
        checkpoint_paths = sorted(
            list(model_folder.glob('*.index')), 
            key=lambda x: int(x.stem.split('-')[-1])
        )
        if len(checkpoint_paths) == 0:
            continue
        checkpoint_path = checkpoint_paths[-1]
        print(f"Using checkpoint {checkpoint_path}")

        checkpoint_name = str(checkpoint_path).replace('.index', '')
        command = ['python3', 'models/research/slim/eval_image_classifier.py',
            '--alsologtostderr',
            '--checkpoint_path', checkpoint_name,
            '--dataset_name', 'visualwakewords',
            '--dataset_split_name', 'val',
            '--dataset_dir', VWW_DATASET,
            '--model_name', model_name,
            '--preprocessing_name', PREPROCESSING_NAME,
            '--train_image_size', str(TRAIN_IMAGE_SIZE),
            '--input_grayscale', 'True']

        log_file.write("NEXT LOG:\n")
        log_file.write(model_name + '\n') 
        result = check_output(command, cwd=str(TF_SOURCE), stderr=subprocess.STDOUT)
        
        for line in result.decode().split('\n'):
            if 'eval/Accuracy' in line:
                try:
                    print(line)
                    acc = line.replace('[', '').replace(']', '').replace('eval/Accuracy', '')
                    print(acc)
                    acc = float(acc)
                    result_dict[model_name] = acc
                    print(result_dict)
                except:
                    print("Error parsing")
                    print(line)
                    
                    
print(result_dict)
        