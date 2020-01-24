"""Copy models into the mbed folder, which should be one directory behind this."""
import argparse
from pathlib import Path

OUTPUT_DIR = Path.cwd().parent / "mbed" / "tensorflow" / "lite" / "micro" / "examples" / "hello_world"
OUTPUT_NAME = "tinyml_model_data"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to model.cc file with the tflite C array models",
        type=str, default="model.cc")
    args = parser.parse_args()


    # We want to automatically generate a header file for these lines
    # Then, copy this header file to
    # ../mbed/tensorflow/lite/micro/examples/hello_world/tinyml_model_data
    text = Path(args.model).read_text()
    header_text = "#ifndef TENSORFLOW_LITE_MICRO_EXAMPLES_MODELS\n"
    header_text += "#define TENSORFLOW_LITE_MICRO_EXAMPLES_MODELS\n\n"

    for line in text.split('\n'):
        # Split out the assignment, add an extern, and add semicolon
        if '=' in line:
            var_assignment = line.split('=')[0]
            header_line = f"extern {var_assignment};"
            header_text += header_line + '\n'

    header_text += "\n#endif"

    # Emit the header and source files to the correct dir
    header_file = OUTPUT_DIR / (OUTPUT_NAME + ".h")
    source_file = OUTPUT_DIR / (OUTPUT_NAME + ".cc")
    header_file.write_text(header_text)
    source_file.write_text(text)
