
import math
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
# calculate hypotenuse for each point in the plane


center_point = (0, 0)
x_range = range(75, 125)
y_range = range(100, 150)

hypotenuse = [
    ((x, y), round(math.sqrt((x - center_point[0]) ** 2 + (y - center_point[1]) ** 2),0)) for x in x_range for y in y_range
]

from collections import defaultdict

groups = defaultdict(list)
for item, length in hypotenuse:
    groups[length].append(item)

# groups is now a dict with lengths as keys
for length, items in groups.items():
    print(length, len(items))

fig, ax = plt.subplots()

for length, items in groups.items():
    x_list, y_list = map(list, zip(*items))
    ax.scatter(x_list, y_list, label=f'Length {length}', s=50,marker='s')


ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.set_aspect('equal')
plt.show()

# 'continuity' check
# for length
# how to check for continuity?
# you need to be able to go from one point to another
# but how to check that?