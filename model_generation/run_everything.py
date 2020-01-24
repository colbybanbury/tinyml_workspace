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
# Assuming all of the models in the models folder.
model_base_folder = Path.cwd() / "models"
model_folders = [a for a in model_base_folder.glob("*")
                 if a.is_dir()]
print(f"Found {len(model_folders)} models to convert.")

# Step 2: Export to frozen protobuf
# Exports into frozen protobufs, with name as the original folder nam
# with _frozen.pb appended to it
# We assume the model folder results will be in the format
# <model_type>-<other_params>
# which will allow us to scrape out the model type easily.
for model_folder in model_folders:
    model_name = model_folder.stem
    model_type = model_name.split('-')[0]
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







