#!/bin/sh
TF_SOURCE=/home/reddilab/packages/tensorflow
DATASET_SOURCE=$TF_SOURCE/models/research/slim/datasets
DATASET_DIR=/home/reddilab/data

cd $DATASET_SOURCE
python3 download_and_convert_visualwakewords.py --logtostderr \
--dataset_name=visualwakewords \
--dataset_dir="${DATASET_DIR}" \
--small_object_area_threshold=0.005 \
--foreground_class_of_interest='person'
cd -
