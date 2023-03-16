import numpy
import pandas as pd
import matplotlib.pyplot as plt
import sys
import string

prefix = sys.argv[1]
timingName = prefix + '-timing.csv'

df = pd.read_csv(timingName, usecols=[0,1,2,3])

print("Timing Data")
print(df)

df = df.rename(str.strip, axis="columns")
print('column names:', df.columns)
df['Hand_Opt'] = (df['RAJA_OpenMP'] - df['Hand_Opt']) / df['Hand_Opt'] * 100
df['LoopChain'] = (df['RAJA_OpenMP'] - df['LoopChain']) / df['LoopChain'] * 100

print("improvement data")
print(df)

df = df.drop(axis=1, labels='RAJA_OpenMP')

print("Plotted data")
print(df)

title="RAJAPerf Performance Improvement"
import seaborn as sns
sns.set()
ax = df.plot(kind='bar',title=title, legend=True, x='Kernel', ylim=(-20,140))
ax.set_xlabel("Benchmark")
ax.set_ylabel("Change in Performance (%)")
plt.xticks(rotation=30, horizontalalignment="right")
plt.legend(loc=(0.72,0.82))
plt.tight_layout(rect=[0,0,1,1])
fig = ax.get_figure()

plt.savefig(prefix + '.png', format='png')


