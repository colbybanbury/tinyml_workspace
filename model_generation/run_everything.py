"""Module that exports everything and turns it into a cpp file
automatically."""
from pathlib import Path
from subprocess import call

def get_most_recent_checkpoint(model_folder):
    """Takes in a model folder path and gets the name of the
    most recent checkpoint."""
    checkpoints = [a.stem for a in model_folder.glob("*.index")]
    latest_checkpoint = sorted(checkpoints, key=lambda x: -int(x.split('-')[-1]))[0]
    return latest_checkpoint


# Step 1: Training
# This script assumes that you have trained everything already
# and each of the trained files is inside a folder already.
# The folder should contain graph.pbtxt
# and some form of model.ckpt-ITERATION NUMBER
model_folders = [a for a in Path.cwd().glob("vww*")
                 if a.is_dir()]

# Step 2: Export to frozen protobuf
# Exports into frozen protobufs, with name as the original folder name
# with _frozen.pb appended to it
model_type = 'mobilenet_v1_0125'
for model_folder in model_folders:
    model_name = model_folder.stem
    frozen_protobuf_name = model_name + '_frozen.pb'
    if Path(frozen_protobuf_name).is_file():
        continue
    checkpoint = model_folder / get_most_recent_checkpoint(model_folder)
    command = f"./export.sh {model_name} {checkpoint} {model_type}"
    print(command)
    call(command, shell=True)


# Step 3: Quantize and convert everything to a C file.
frozen_protobufs = [folder.stem + "_frozen.pb" for folder in model_folders]
for frozen_protobuf in frozen_protobufs:
    call(['python3', 'convert.py', '--model', frozen_protobuf])







