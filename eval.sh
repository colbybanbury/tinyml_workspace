#!/bin/sh
TF_SOURCE=$HOME/packages/tensorflow
VWW_DATASET=$TF_SOURCE/models/research/slim/mscoco
PY=python3
CHECKPOINT=$(pwd)/$1

cd $TF_SOURCE
$PY models/research/slim/eval_image_classifier.py \
--alsologtostderr \
--checkpoint_path=$CHECKPOINT \
--dataset_dir=$VWW_DATASET \
--dataset_name=visualwakewords \
--dataset_split_name=val \
--model_name=mobilenet_v1_025 \
--preprocessing_name=mobilenet_v1 \
--input_grayscale=True \
--train_image_size=96
cd -
