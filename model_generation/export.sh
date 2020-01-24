#!/bin/sh
# Saves and freezes a model checkpoint that we trained
# Usage:
#   ./export.sh <my_name_for_model> <model checkpoint file>
# You need to put your tensorflow path to make it work.
# If there are errors, once you clone tensorflow
# I would advise checking out the 1.15 branch.
#   git checkout r1.15
# because tensorflow devs break everything with each update
TF_SOURCE=$HOME/packages/tensorflow
PY=python3
CWD=$(pwd)
SAVE_FILE=$CWD/$1
CHECKPOINT=$2
MODEL_NAME=$3

cd $TF_SOURCE
$PY models/research/slim/export_inference_graph.py \
--alsologtostderr \
--dataset_name=visualwakewords \
--model_name=$MODEL_NAME \
--image_size=96 \
--input_grayscale=True \
--output_file=$SAVE_FILE.pb
cd -

$PY $TF_SOURCE/tensorflow/python/tools/freeze_graph.py \
--input_graph=$SAVE_FILE.pb \
--input_checkpoint=$CHECKPOINT \
--input_binary=true \
--output_graph=${SAVE_FILE}_frozen.pb \
--output_node_names=MobilenetV1/Predictions/Reshape_1
