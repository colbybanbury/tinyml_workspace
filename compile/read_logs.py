"""parsing the results from our logs."""
import pandas as pd
from pathlib import Path
from info import OPCODE2NAME

log_path = Path("mbed_results") / "NUCLEO_F767ZI.log"

def opcode_to_name(opcode):
    try:
        return OPCODE2NAME[opcode]
    except IndexError:
        return "unknown/custom"

def chunk_to_dataframe(chunk):
    chunk = chunk.strip()
    
    # The chunks will be preceded by the model name.
    # then, the format is
    # opcode\tlayer_version\tinference_time
    model_name = chunk.split('\n')[0]
    layer_times = chunk.split('\n')[1:-1]

    data = []
    for idx, layer_info in enumerate(layer_times):
        items = layer_info.split('\t')
        opcode = int(items[0])
        version = int(items[1])
        time = float(items[2])
        data.append((model_name, idx, opcode, version, time))
    df = pd.DataFrame(data)
    df.columns = ['model_name', 'layer_num', 'opcode', 'opcode_version', 'time']
    return df
 

text = log_path.read_text()
record_dfs = []
for chunk in text.split("START_BENCHMARKING"):
    if 'END_BENCHMARKING' not in chunk:
        continue
    df = chunk_to_dataframe(chunk)
    record_dfs.append(df)

result_df = pd.concat(record_dfs)
print(result_df)
print(result_df.info())
result_df['layer_name'] = result_df.apply(
    lambda row: opcode_to_name(row['opcode']) + '_' + str(row['layer_num']), axis=1)
print(result_df)
