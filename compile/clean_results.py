from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

sns.set('talk')

log_file = Path.cwd() / 'mbed_results' / 'NUCLEO_F767ZI.log'

text = log_file.read_text()
records = []
for line in text.split('\n'):
    if line.count(',') == 2:
        try:
            info = line.split('<')
            model_name = info[1]
            time = info[2]
            model_name = model_name.strip().replace('>', '').replace(',', '')
            time = time.strip().replace('>', '').replace(',', '') 
            time = float(time.replace('seconds', ''))
            records.append((model_name, time))
        except:
            pass

df = pd.DataFrame(records)
df.columns = ['model_name', 'time']
df['mobilenet_width'] = df.model_name.map(
        lambda x: float(x.split('_')[2])) / 100.

sns.lineplot(data=df, x='mobilenet_width', y='time', marker='o') 
plt.title("Mobilenet width parameter performance in Cortex-M7 MCU")
plt.xlabel("Width scaling")
plt.ylabel("Inference Time, VWW")
plt.show()

