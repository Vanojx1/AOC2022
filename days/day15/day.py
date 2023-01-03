import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from itertools import cycle
from functools import reduce

color_list = cycle(list(mcolors.CSS4_COLORS.keys())[8:])

def dist(a, b): return abs(b[0]-a[0]) + abs(b[1]-a[1])

def main(day_input):
    Y, XYLIMIT = 2000000, 4000000

    sensors = {}
    for row in day_input:
        sx, sy, bx, by = map(int, re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', row).groups())
        sensors[(sx, sy)] = dist((sx, sy), (bx, by))

    plt.axes()

    for s, d in sensors.items():
        if Y > s[1]+d or Y < s[1]-d: continue
        c = next(color_list)
        pts = [[s[0]+d, s[1]], [s[0], s[1]+d], [s[0]-d, s[1]], [s[0], s[1]-d]]
        area = plt.Polygon(pts, closed=True, fc=c,alpha=0.8)
        plt.gca().add_patch(area)

    def calc_pairs_at_y(curr_y):
        pairs = []
        int_points = set([])
        for s, d in sensors.items():
            if curr_y > s[1]+d or curr_y < s[1]-d: continue
            x1, x2 = -(d-abs(s[1]-curr_y))+s[0], (d-abs(s[1]-curr_y))+s[0]
            int_points |= set([x1, x2])
            pairs.append((x1, x2))
        return int_points, pairs

    int_points, _ = calc_pairs_at_y(Y)

    distress_beacon = None
    for curr_y in range(Y+1, XYLIMIT+1):
        if distress_beacon: break
        _, pairs = calc_pairs_at_y(curr_y)
        flatten_pairs = reduce(lambda c, n: c + [(n[0], 'o'), (n[1], 'c')], pairs, [])
        sorted_pairs = sorted(flatten_pairs, key=lambda x: x[0])

        o = 1
        for i, (n, oc) in enumerate(sorted_pairs[1:-1]):
            np, _ = sorted_pairs[i+2]
            if oc == 'o': o += 1
            else: o -= 1
            if o == 0 and np-n >= 2:
                distress_beacon = (n+1, curr_y)
                break

    plt.plot(*distress_beacon, 'o', color='red')

    plt.axhline(0, color='black')
    plt.axhline(Y, color='r')
    plt.axhline(XYLIMIT, color='black')
    plt.axvline(0, color='black')
    plt.axvline(XYLIMIT, color='black')
    plt.axis('scaled')
    # plt.show()

    return max(int_points)-min(int_points), distress_beacon[0]*4000000+distress_beacon[1]