import re, heapq
from collections import defaultdict
from itertools import combinations

def main(day_input):
    rates = {}
    valve_connections = {}
    for row in day_input:
        valve, rate, dest = [f(v) for v, f in zip(re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w+(?:, )?)+)', row).groups(), [lambda x:x, int, lambda x:x.split(', ')])]
        rates[valve] = rate
        valve_connections[valve] = dest

    def calc_paths(valve):
        q = [(1, [valve])]
        heapq.heapify(q)

        seen = set([valve])
        can_reach = []
        while q:

            steps, path = heapq.heappop(q)
            curr_valve = path[-1]

            for next_valve in valve_connections[curr_valve]:
                if next_valve not in seen:
                    can_reach.append((steps + 1, next_valve))
                    heapq.heappush(q, (steps + 1, path + [next_valve]))
                    seen.add(next_valve)

        return can_reach

    TIME_LIMIT = 30

    valve_map = {}
    for valve in valve_connections.keys():
        if rates[valve] == 0 and valve != 'AA': continue
        valve_map[valve] = sorted([(s, v) for s, v in calc_paths(valve) if rates[v] > 0], key=lambda x: rates[x[1]], reverse=True)

    def gen_path_map(p2=False):
        rmap = defaultdict(int)
        def set_map(p, u):
            nonlocal rmap
            su = tuple(sorted(u[1:]))
            if p > rmap[su]:
                rmap[su] = p
                yield su, (p, set(u[1:]))

        def r(p=0, t=TIME_LIMIT, u=['AA']):
            if len(u) > 1: yield from set_map(p, u)
            for s, n in valve_map[u[-1]]:
                if t-s <= 0:
                    yield from set_map(p, u)
                    continue
                if n in u: continue
                yield from r(p+rates[n]*(t-s), t-s, u+[n])

        return {k: v for k, v in r(0, TIME_LIMIT - (4 if p2 else 0))}

    rmap1 = gen_path_map()
    rmap2 = gen_path_map(True)

    return max(rmap1.values())[0], max(p1+p2 for (p1, u1), (p2, u2) in combinations(sorted(rmap2.values(), reverse=True), 2) if not (u1 & u2))

