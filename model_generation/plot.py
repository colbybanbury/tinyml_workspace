"""Plot accuracy vs model size for our visual wake word trained models."""
import seaborn as sns
from matplotlib import pyplot as plt
from pathlib import Path
import pandas as pd

accuracy = Path.cwd() / 'accuracy.log'
sizes = Path.cwd() / "sizes.log"


acc_dict = eval(accuracy.read_text())
size_dict = eval(sizes.read_text())

data = []
for model_name in acc_dict.keys():
    data.append((model_name, acc_dict[model_name], size_dict[model_name]))

df = pd.DataFrame(data)
df.columns = ['model', 'accuracy', 'size']
print(df)


sns.scatterplot(y='accuracy', x='size', data=df)
plt.title("Visual Wake Words Model Test")
plt.xlabel("Bytes")
plt.ylabel("Dev set accuracy")
plt.show()