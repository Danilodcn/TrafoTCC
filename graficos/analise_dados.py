import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

file_name = "individuos.xlsx"
table = pd.read_excel(file_name, index_col=0)
print(table)

# plt.figure()
# sns.heatmap(table.corr(), annot=True, cmap="Wistia")
sns.pairplot(table)


plt.show()