"""A python version of the training script. Goes through a few parameters
and places all of the training models into individual folders."""

from subprocess import call
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

# Model parameters that we would like to use.
PREPROCESSING_NAME = 'mobilenet_v1'  # method of preprocessing training data
TRAIN_IMAGE_SIZE = 96



model_names = ['mobilenet_v1_%.03d' % width for width in
               [16, 14, 12, 10, 8, 6, 4]]
for model_name in model_names:
    command = ['python3', 'models/research/slim/train_image_classifier.py'
        '--train_dir', model_name,
        '--dataset_name', 'visualwakewords',
        '--dataset_split_name', 'train',
        '--dataset_dir', VWW_DATASET,
        '--model_name', model_name,
        '--preprocessing_name', PREPROCESSING_NAME,
        'train_image_size', TRAIN_IMAGE_SIZE,
        '--input_grayscale', 'True', 
        '--save_summaries_secs', '300',
        '--learning_rate', 0.045,
        '--label_smoothing', 0.1,
        '--learning_rate_decay_factor', 0.98,
        '--num_epochs_per_decay', 2.5,
        '--moving_average_decay', 0.9999,
        '--batch_size', 96,
        '--max_number_of_steps', 10000]
    call(command, cwd=TF_SOURCE)