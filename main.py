
import math
import numpy as np
from collections import defaultdict
#from matplotlib import pyplot as plt
#from matplotlib.ticker import MultipleLocator
# calculate hypotenuse for each point in the plane

def calculate_number_of_adjacent_points(point, set):
    adjacent_number = 0
    x, y = point
    # Check all 8 possible adjacent points
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            adjacent_point = (x + dx, y + dy)
            if adjacent_point in set:
                adjacent_number += 1
    return adjacent_number

center_point = (0, 0)
tested_range = 10000  # from -tested_range to +tested_range

# Step 1: coordinate grids
coords = np.arange(-tested_range, tested_range + 1, dtype=np.int32)
X, Y = np.meshgrid(coords, coords, indexing="xy")

# Step 2: integer distances
distances = np.rint(np.hypot(X - center_point[0], Y - center_point[1])).astype(np.int32)
print("Hypotenuse for all points calculated.")

# Step 3: group points by distance
points_by_dist = defaultdict(list)
for x, y, r in zip(X.ravel(), Y.ravel(), distances.ravel()):
    points_by_dist[r].append((x, y))
print("Points grouped by distance, ready.")




# groups is now a dict with lengths as keys
#for length, items in groups.items():
#    print(length, items)

#fig, ax = plt.subplots()
"""
for length, items in groups.items():
    x_list, y_list = map(list, zip(*items))
    ax.scatter(x_list, y_list, label=f'Length {length}', s=50,marker='s')

ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.set_aspect('equal')
plt.show()
"""
result = defaultdict(list)
for length, items in points_by_dist.items():
    if length % 100 == 0:
        print(f"Testing length {length}...")
    more_than_2 = True
    items_as_set = set(items)
    for item in items:
        adjacent_count = calculate_number_of_adjacent_points(item, items_as_set)
        if adjacent_count < 2:
            more_than_2 = False
            break
    result[length] = more_than_2


all_tested_pass = True
for n in range(1, tested_range + 1):
    if result[n] is True:
        continue
    else:
        print(f"Test failed for length {n}")
        all_tested_pass = False

print("All tests passed!" if all_tested_pass else "Some tests failed.")
print("In range 1 to", tested_range, "all points have at least 2 adjacent points.")