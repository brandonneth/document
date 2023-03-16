
manual_changed = [6,2,1,8,4,3,10,12]
manual_added = [6,3,1,4,41,17,33,38]
lc_changed = [6,2,2,9,3,3,10,12]
lc_added = [2,2,2,4,2,3,3,3]

from scipy import stats

av1 = stats.gmean(manual_changed)
av2 = stats.gmean(manual_added)
av3 = stats.gmean(lc_changed)
av4 = stats.gmean(lc_added)

print(av1,av2)
print(av3,av4)

print('arithmetic')
print(sum(manual_changed) / 8)
print(sum(manual_added) / 8)
print(sum(lc_changed) / 8)
print(sum(lc_added) / 8)
print()