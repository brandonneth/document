import sys
import os
import re
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def filename_to_values(filename):
	iterations = -1
	variant = -1
	size = -1
	pattern = r'v(?P<Variant>\d+)_i(?P<Iterations>(all)|\d+)_s(?P<Size>\d+)(_r(?P<runNum>\d+))?.out'
	result = re.match(pattern, filename)
	print(result)
	if result:
		variant = int(result.group('Variant'))
		if result.group("Iterations") != 'all':
			iterations = int(result.group('Iterations'))
		size = int(result.group('Size'))
	
	return (variant, iterations, size)

def execution_time(filename):
	file = open(filename, "r")
	contents = file.read()
	lines = contents.split("\n")
	if len(lines) < 25:
		return None
	timeline = lines[24]
	print(timeline)
	pattern = r'Elapsed time\s*=\s*(?P<time>\d+.\d+).* \(s\)'
	result = re.match(pattern, timeline)
	if result:
		print("extracted time:", result.group("time"))
		return float(result.group("time"))
	print("no time found")
	return None


data = []



dirname = str(os.path.basename(os.getcwd()))
files = [f for f in os.listdir() if os.path.isfile(os.path.join(os.curdir, f)) and f.endswith(".out")]

print('files in cur directory:', files)

variant_map = {0 : 'Original', 7 : 'RAJALC', 9 : 'By Hand'}

for filename in files:
	print("Extracting from ", filename)	
	(variant,iterations,size) = filename_to_values(filename)
	exec_time = execution_time(filename)

	variant = variant_map[variant]
	if exec_time is not None:
		data += [[variant, iterations, size, exec_time]]

data.sort()
print('data:', data)


df = pd.DataFrame(data, columns=["Variant", "Iterations", "Size", "ExecTime"])
print('dataframe:')
print(df)

df = df.pivot_table(index='Size',columns='Variant',values='ExecTime',aggfunc=np.mean)
print('pivoted:')
print(df)

df = df[['Original', 'RAJALC', 'By Hand']]

print('reindexed:')
print(df)

df['RAJALC'] = df['Original']/df['RAJALC']
df['By Hand'] = df['Original']/df['By Hand']

df['Original'] = df['Original']/df['Original']

print("scaled:")
print(df)

print(df.columns)


import seaborn as sns
sns.set()
ax = df.plot(kind='bar',legend=True)
ax.set_xlabel("Problem Size")
ax.set_ylabel("Speedup")
plt.xticks(rotation=0)
plt.legend(loc=(1.04,0))
plt.tight_layout(rect=[0,0,1,1])
fig = ax.get_figure()


#graph = sns.barplot(df,x=df.index, hue=df.columns.name)


plt.show()


fig.savefig(dirname + '.png', format="png", bbox_inches="tight")

