
import json
import numpy as np
from matplotlib import pyplot as plt


len(ids)
plt.plot(ids)

np.arange(len(ids))
np.array(ids)

c = comps[5]
c['cats']

iyears = list(range(2001, 2019))

cpy = np.array([(y, len([c for c in comps if c['date'].split('.')[2] == str(y)])) for y in years])
cpm = np.array([(m, len([c for c in comps if c['date'].split('.')[1] == f'{m:02d}'])) for m in range(1, 13)])


# %% Analyze couple IDs

results = json.load(open('data/vysledky.json', 'r'))
ids = [int(c['couple_id']) for r in results.values() for c in r['results']]

arr = np.array(ids)
# Get missing observations
m = np.sort(np.setdiff1d(np.arange(1, max(arr)+1), arr))
# Missing observations are arranged in continuous intervals. Get the bounds of the intervals
steps = np.array([m[:-1], m[1:]])[:, m[1:] - m[:-1] > 1]
# Inclusive ranges of missing observations
intervals = np.array([np.insert(steps[1], 0, m[0]), np.append(steps[0], m[-1])]).T


# %%


cpy[:,0]
plt.step(cpy[:,0], cpy[:,1])
plt.xlabel('Rok')
plt.ylabel('Celkový počet soutěží')
_ = plt.xticks(list(range(2001, 2019)), rotation=60)
plt.grid(True)

plt.figure()

plt.bar(cpm[:,0], cpm[:,1] / len(years))
plt.xlabel('Měsíc')
plt.ylabel('Průměrný počet soutěží')
_ = plt.xticks(list(range(1, 13)), rotation=60)
# plt.grid(True)
