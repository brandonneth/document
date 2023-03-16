import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import string



dfs = []


def clean(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	outlines = []
	for line in lines:
		if line not in ['Speedup Report (T_ref/T_var): ref var = RAJA_OpenMP  ,  ,  ,\n', 'Mean Runtime Report (sec.)  ,  ,  , \n']:
			outlines += [line]
	
	f.close()
	f = open(filename, 'w')
	f.writelines(outlines)
	f.close()



midfix = 'threads'
for prefix in ['lassen-fusion', 'tiling']:
	for num in [1,2,4,8,16,32]:
		timingName = 'lassen/' + prefix + "-" + str(num) + midfix + "-timing.csv"
		clean(timingName)

		df = pd.read_csv(timingName, usecols=[0,1,2,3])

		df = df.rename(str.strip, axis="columns")
		for label in ['Apps_', 'Lcals_', 'Polybench_']:
			df['Kernel'] = df['Kernel'].str.replace(label, '')
		df['Kernel'] = df['Kernel'].str.strip()
		#df['Hand_Opt'] = (df['RAJA_OpenMP'] - df['Hand_Opt']) / df['Hand_Opt'] * 100
		#df['LoopChain'] = (df['RAJA_OpenMP'] - df['LoopChain']) / df['LoopChain'] * 100
		#df['RAJA_OpenMP'] = (df['RAJA_OpenMP'] - df['RAJA_OpenMP']) / df['RAJA_OpenMP'] * 100
		df['Threads'] = num
		df['System'] = 'Power9'
		#df = df.drop(columns=['RAJA_OpenMP'])

		dfs += [df]

midfix = 'thread'
for (prefix,midfix) in [('fusion','thread'), ('tiling','threads')]:
	for num in [1,2,4,8,16,32]:
		timingName = 'quartz/run2/' + prefix + "-" + str(num) + midfix + "-timing.csv"
		clean(timingName)

		df = pd.read_csv(timingName, usecols=[0,1,2,3])

		df = df.rename(str.strip, axis="columns")
		for label in ['Apps_', 'Lcals_', 'Polybench_']:
			df['Kernel'] = df['Kernel'].str.replace(label, '')
		df['Kernel'] = df['Kernel'].str.strip()
		#df['Hand_Opt'] = (df['RAJA_OpenMP'] - df['Hand_Opt']) / df['Hand_Opt'] * 100
		#df['LoopChain'] = (df['RAJA_OpenMP'] - df['LoopChain']) / df['LoopChain'] * 100
		#df['RAJA_OpenMP'] = (df['RAJA_OpenMP'] - df['RAJA_OpenMP']) / df['RAJA_OpenMP'] * 100
		df['Threads'] = num
		df['System'] = 'x86-64'
		#df = df.drop(columns=['RAJA_OpenMP'])

		dfs += [df]
combined = pd.concat(dfs)
print('combined')
print(combined)

df = combined.pivot(index="Kernel", columns=['System', 'Threads'])
df = df.reindex(axis='index', labels=['ENERGY', 'FDTD_2D', 'GEN_LIN_RECUR', 'PRESSURE', 'JACOBI_1D', 'JACOBI_2D', 'HEAT_3D', 'HYDRO_2D'])
#df = df.reindex(['ENERGY', 'FDTD_2D', 'GEN_LIN_RECUR', 'PRESSURE', 'JACOBI_1D', 'JACOBI_2D', 'HEAT_3D', 'HYDRO_2D'])
print("after pivot and reindex")
print(df)


print("df.T")
print(df.T)





for version in ['LoopChain', 'Hand_Opt', 'RAJA_OpenMP']:
	for thread in [32,16,8,4,2,1]:
		#print(version , ":", thread)
		#print(df[version][thread])
		reference = df['RAJA_OpenMP'][1]
		df[version][thread] = reference / df[version][thread]

print("swap")
df = df.swaplevel(i=0, j=1, axis='columns')
print(df)

df = df.sort_index(axis='columns')
print('after second reindex')
print(df)

from scipy import stats
df.loc['Geometric Mean'] = stats.gmean(df.loc[:])

print(df)
import seaborn as sns

if len(sys.argv) > 1:
	title = sys.argv[1]
else:
	title = ''

sns.set()
ax = df.plot(kind='bar',title=title, legend=True, ylim=(0,20))
ax.set_xlabel("Benchmark")
ax.set_ylabel("Speedup")
plt.xticks(rotation=30)
plt.legend(loc=(1,0))

ax.text(6.2,20,'29.23', fontsize=10)


handles,labels=ax.get_legend_handles_labels()

#permutation = lambda i : [0,4,1,5,2,6,3,7][i]

#newHandles = [handles[permutation(i)] for i in range(0,8)]
#newLabels = [labels[permutation(i)] for i in range(0,8)]

#ax.legend(newHandles,newLabels, loc=(1.02,0))
plt.tight_layout(rect=[0,0,1,1])
fig = ax.get_figure()

plt.savefig('scaling.png', format='png')

plt.show()

#df = df.swaplevel(i=0, j=1, axis='columns')



