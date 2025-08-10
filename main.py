
import math
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
# calculate hypotenuse for each point in the plane



def check_if_each_point_has_two_neighbors(points):
    """Check if each point has at least two neighbors."""
    _NEIGH = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    s = set(points)
    for x, y in points:
        cnt = 0
        for dx, dy in _NEIGH:
            if (x + dx, y + dy) in s:
                cnt += 1
                if cnt >= 2:
                    break
        if cnt < 2:
            return False
    return True

center_point = (0, 0)
tested_range = 1_000_000_000  # from -tested_range to +tested_range

# Step 1: coordinate grids
x_coords = np.arange(tested_range-50, tested_range + 1, dtype=np.int32)
y_coords = np.arange(tested_range-50, tested_range + 1, dtype=np.int32)

X, Y = np.meshgrid(x_coords, y_coords, indexing="xy")

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

fig, ax = plt.subplots()

for length, items in points_by_dist.items():
    x_list, y_list = map(list, zip(*items))
    ax.scatter(x_list, y_list, label=f'Length {length}', s=50, marker='s')

ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.set_aspect('equal')
plt.show()



