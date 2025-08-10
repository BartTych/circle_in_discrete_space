import math
from collections import defaultdict

def ring_points(r: int):
    """
    All integer (x,y) with (r-0.5)^2 <= x^2+y^2 < (r+0.5)^2
    Generated per x; uses symmetry implicitly by scanning full range.
    Returns a list of (x,y) tuples.
    """
    rp = r + 0.5
    rm = max(0.0, r - 0.5)
    rp2 = rp * rp
    rm2 = rm * rm

    pts = []
    # For large r, |x| > rp gives no solutions
    xmin = -int(math.floor(rp))
    xmax =  int(math.floor(rp))
    for x in range(xmin, xmax + 1):
        x2 = x * x
        # if even the closest y (y=0) is outside the ring, skip fast
        if x2 >= rp2:  # then x^2 + y^2 >= rp^2 for any |y|>=0
            continue

        # upper bound for |y|: floor(sqrt(rp^2 - x^2))
        ymax = int(math.floor(math.sqrt(max(0.0, rp2 - x2))))

        # lower bound for |y|: ceil(sqrt(max(0, rm^2 - x^2)))
        ymin_sq = rm2 - x2
        if ymin_sq <= 0:
            ymin = 0
        else:
            ymin = int(math.ceil(math.sqrt(ymin_sq)))

        if ymin > ymax:
            continue

        # add both signs; include y=0 only once
        if ymin == 0:
            pts.append((x, 0))
            for y in range(1, ymax + 1):
                pts.append((x,  y))
                pts.append((x, -y))
        else:
            for y in range(ymin, ymax + 1):
                pts.append((x,  y))
                pts.append((x, -y))
    return pts

# 8-neighborhood offsets
_NEIGH = [(-1,-1), (-1,0), (-1,1),
          ( 0,-1),         ( 0,1),
          ( 1,-1), ( 1,0), ( 1,1)]

# Clockwise neighbor order starting at (1,0)
_NEIGH_CW = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
# 3×3 grid positions (top-left → bottom-right); center at index 4
_GRID_3x3 = [(-1, 1), (0, 1), (1, 1),
             (-1, 0), (0, 0), (1, 0),
             (-1,-1), (0,-1), (1,-1)]

def neighborhood_mask_9(x, y, s):
    mask = 0
    for i, (dx, dy) in enumerate(_GRID_3x3):
        if (x + dx, y + dy) in s:
            mask |= (1 << i)
    return mask

def check_and_collect_configs(points, configs_set, forbidden_set=None):
    """
    - Enforces: ≥2 neighbors; if exactly 2, they must not be consecutive (including wrap 7–0).
    - Always records the 3×3 neighborhood mask for points with exactly 2 neighbors
      into `configs_set`, even if the pair is forbidden.
    - If `forbidden_set` is provided, also records masks of the forbidden cases there.
    """
    s = set(points)
    for x, y in points:
        idx = []
        for k, (dx, dy) in enumerate(_NEIGH_CW):
            if (x + dx, y + dy) in s:
                idx.append(k)
                if len(idx) == 3:  # >2 neighbors ⇒ automatically OK
                    break

        # record mask unconditionally for debugging
        m = neighborhood_mask_9(x, y, s)
        configs_set.add(m)

        if len(idx) < 2:
            return False

        if len(idx) == 2:
            a, b = idx[0], idx[1]
            d = (b - a) % 8

            

            # forbid consecutive (including wrap pair 7–0)
            if d in (1, 7):
                if forbidden_set is not None:
                    forbidden_set.add(m)
                return False
    return True

def all_points_two_neighbors_nonconsecutive(points):
    s = set(points)
    for x, y in points:
        idx = []
        for k, (dx, dy) in enumerate(_NEIGH_CW):
            if (x + dx, y + dy) in s:
                idx.append(k)
                if len(idx) == 3:   # >2 neighbors → automatically OK; no need to gather more
                    break

        if len(idx) < 2:
            return False

        if len(idx) == 2:
            a, b = idx[0], idx[1]
            d = (b - a) % 8
            # forbid consecutive positions: 1 (next clockwise) or 7 (next counter-clockwise / wrap 7↔0)
            if d in (1, 7):
                return False
    return True


def all_points_have_two_neighbors_strict(points):
    s = set(points)
    for x, y in points:
        neigh = []
        for dx, dy in _NEIGH:
            if (x + dx, y + dy) in s:
                neigh.append((x + dx, y + dy))
                if len(neigh) > 2:  # no need to collect more for the rule
                    break

        if len(neigh) < 2:
            return False

        if len(neigh) == 2:
            (x1, y1), (x2, y2) = neigh
            # Are the two neighbors adjacent to each other (8-neighborhood)?
            if max(abs(x1 - x2), abs(y1 - y2)) <= 1:
                return False
    return True

def all_points_have_two_neighbors(points):
    s = set(points)
    for x, y in points:
        cnt = 0
        # early exit after reaching 2
        for dx, dy in _NEIGH:
            if (x + dx, y + dy) in s:
                cnt += 1
                if cnt >= 2:
                    break
        if cnt < 2:
            return False
    return True

def pretty_mask(mask):
    """Convert a 9-bit mask to a 3×3 text representation."""
    chars = []
    for i in range(9):
        chars.append('#' if (mask >> i) & 1 else '.')
    return '\n'.join(''.join(chars[r*3:(r+1)*3]) for r in range(3))

def pretty_mask_with_center(mask):
    chars = []
    for i in range(9):
        if i == 4:  # center index
            chars.append('O')
        else:
            chars.append('#' if (mask >> i) & 1 else '.')
    return '\n'.join(''.join(chars[r*3:(r+1)*3]) for r in range(3))

# -------- main ----------
tested_range = 120  # from -tested_range to +tested_range

points_by_dist = defaultdict(list)
result = []
set_of_configs = set()
for r in range(1, tested_range + 1):
    pts = ring_points(r)
    points_by_dist[r] = pts  # if you actually need this dictionary
    ok = check_and_collect_configs(pts,set_of_configs)
    if not ok:
        print(f"FAIL for r={r}")
    result.append(ok)
    #if r % 100 == 0:
    print(f"r={r}: |pts|={len(pts)} -> {'OK' if ok else 'FAIL'}")

# final check
all_tested_pass = all(result)
print("All tests passed!" if all_tested_pass else "Some tests failed.")

print(f"Total configurations found: {len(set_of_configs)}")
print("Sample configurations (masks):")
print(set_of_configs)

for m in sorted(set_of_configs):
    print(f"Mask {m}:\n{pretty_mask_with_center(m)}\n")

print('size of set_of_configs:', len(set_of_configs))