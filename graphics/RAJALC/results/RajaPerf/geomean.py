

import numpy
import pandas as pd
import matplotlib.pyplot as plt
import sys
import string

prefix = sys.argv[1]


def clean(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	outlines = []
	for line in lines:
		if line not in ['Speedup Report (T_ref/T_var): ref var = RAJA_OpenMP  ,  ,  , \n', 'Mean Runtime Report (sec.)  ,  ,  , \n']:
			outlines += [line]
	
	f.close()
	f = open(filename, 'w')
	f.writelines(outlines)
	f.close()


timingName = prefix + "-speedup.csv"
clean(timingName)


df = pd.read_csv(timingName, usecols=[0,1,2,3])

df = df.rename(str.strip, axis="columns")
print(df)
df['Kernel'] = df['Kernel'].str.strip()

print(df)

df['Difference'] = (df['LoopChain']-1) / (df['Hand_Opt']-1)

print(df)

from scipy import stats
geomean = stats.gmean(df['Difference'])
print('geomean:', geomean)