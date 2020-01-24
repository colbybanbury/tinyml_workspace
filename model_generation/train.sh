#!/bin/sh
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
TF_SOURCE=$HOME/packages/tensorflow
VWW_DATASET=$TF_SOURCE/models/research/slim/mscoco
PREPROCESSING_NAME=mobilenet_v1
# MODEL_NAME=mobilenet_v1_025
# MODEL_NAME=mobilenet_v1_0125
# To add mobilenet models with different width parameters, simply add them to the tensorflow
# source at the location:
#
#   tensorflow/models/research/slim/nets/mobilenet_v1.py
#   tensorflow/models/research/slim/nets/nets_factory.py
TRAIN_IMAGE_SIZE=96  # default is 96

cd $TF_SOURCE
chmod +x models/research/slim/datasets/download_mscoco.sh
bash models/research/slim/datasets/download_mscoco.sh coco
cd -

for MODEL_NAME in \
mobilenet_v1_016 \
mobilenet_v1_014 \
mobilenet_v1_012 \
mobilenet_v1_010 \
mobilenet_v1_008 \
mobilenet_v1_006 \
mobilenet_v1_004 ; do
training_directory=vww_${MODEL_NAME}
# Train the model with different image sizes
python3 $TF_SOURCE/models/research/slim/train_image_classifier.py \
--train_dir=$training_directory \
--dataset_name=visualwakewords \
--dataset_split_name=train \
--dataset_dir=$VWW_DATASET \
--model_name=$MODEL_NAME \
--preprocessing_name=$PREPROCESSING_NAME \
--train_image_size=$TRAIN_IMAGE_SIZE \
--input_grayscale=True \
--save_summaries_secs=300 \
--learning_rate=0.045 \
--label_smoothing=0.1 \
--learning_rate_decay_factor=0.98 \
--num_epochs_per_decay=2.5 \
--moving_average_decay=0.9999 \
--batch_size=96 \
--max_number_of_steps=3000
done




