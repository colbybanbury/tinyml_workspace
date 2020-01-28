"""Gets the sizes of the models from the model.cc file"""
from pathlib import Path

model_file = Path.cwd() / 'model.cc'
text = model_file.read_text()

model_sizes = {}
for line in text.split('\n'):
    if '=' in line and '_len' in line:
        num_bytes = int(line.replace(';', '').strip().split(' ')[-1])
        model_name = line.strip().split(' ')[2].replace('_frozen', '').replace('_len', '')
        print(num_bytes)
        print(model_name)
        model_sizes[model_name] = num_bytes

print(model_sizes)
