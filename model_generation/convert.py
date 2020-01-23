"""Quantize our model into tflite format."""
import argparse
import tensorflow as tf
import io
import PIL
import os
import numpy as np
import tempfile
from subprocess import call
from pathlib import Path


def generate_representative_data():
    """Generate our dataset used to train. Allows the quantizer to know what
    the range of inputs will be in order to quantize more efficiently."""
    record_iterator = tf.python_io.tf_record_iterator(
        path=os.path.join(args.data, 'val.record-00000-of-00010'))

    count = 0
    for string_record in record_iterator:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        image_stream = io.BytesIO(example.features.feature['image/encoded'].bytes_list.value[0])
        image = PIL.Image.open(image_stream)
        image = image.resize((96, 96))
        image = image.convert('L')
        array = np.array(image)
        array = np.expand_dims(array, axis=2)
        array = np.expand_dims(array, axis=0)
        array = ((array / 127.5) - 1.0).astype(np.float32)
        yield([array])
        count += 1
        if count > 300:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", type=str,
        default="/home/reddilab/packages/tensorflow/models/research/slim/mscoco",
        help='Path to mscoco data')
    parser.add_argument("-m", "--model", type=str,
        help='Path to frozen model that should be quantized')
    parser.add_argument("-o", "--output", default=None,
        help='output name for your new C array corresponding to model')
    args = parser.parse_args()

    converter = tf.lite.TFLiteConverter.from_frozen_graph(
        args.model, ['input'], ['MobilenetV1/Predictions/Reshape_1'])
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # TODO: enable data level quantization again later, some bug
    # converter.representative_dataset = generate_representative_data
    tflite_quant_model = converter.convert()

    if args.output is None:
        args.output = Path(args.model).stem


    tmpdir = Path('/tmp')
    output_file = tmpdir / args.output
    with output_file.open('wb') as tflite_model:
        tflite_model.write(tflite_quant_model)
    cc_path = Path.cwd() / 'model.cc'
    command = f"xxd -i {output_file.name} >> {cc_path}"
    print(command)
    call(command, shell=True, cwd=tmpdir)
    
    

