
import json
import numpy as np
from matplotlib import pyplot as plt

comps = json.load(open('data/souteze.json', 'r'))
years = list(range(2001, 2019))

cpy = np.array([(y, len([c for c in comps if c['date'].split('.')[2] == str(y)])) for y in years])
cpm = np.array([(m, len([c for c in comps if c['date'].split('.')[1] == f'{m:02d}'])) for m in range(1, 13)])

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
