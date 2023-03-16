import numpy
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
for prefix,midfix in [('fusion','thread'), ('tiling','threads')]:
	for num in [1,2,4,8,16,32]:
		timingName = prefix + "-" + str(num) + midfix + "-timing.csv"
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
		#df = df.drop(columns=['RAJA_OpenMP'])

		dfs += [df]

combined = pd.concat(dfs)
print('combined')
print(combined)

df = combined.pivot(index="Kernel", columns='Threads')
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

numDifferent = 0
numSame = 0

for thread in [1,2,4,8,16,32]:
	for kernel in ['ENERGY', 'FDTD_2D', 'GEN_LIN_RECUR', 'PRESSURE', 'JACOBI_1D', 'JACOBI_2D', 'HEAT_3D', 'HYDRO_2D']:
		handSpeed = df['Hand_Opt'][thread][kernel]
		lcSpeed = df['LoopChain'][thread][kernel]
		if ((handSpeed < 1) == (lcSpeed < 1)):
			numSame += 1
		else:
			numDifferent += 1
			print("Different for ", kernel, thread)

print("Count with same direction: ", numSame)
print("Count with different direction: ", numDifferent)