import re, copy
from collections import defaultdict

def format(stacks):
    return ''.join([(v or [''])[-1] for k, v in sorted(stacks.items())])

def main(day_input):
    
    stacks = defaultdict(list)
    for row in day_input:
        if not row: break
        m = re.findall(r'(?:(?:(?:\[(\w)\])|(?:\s{3})) ?)', row)
        for i, crate in enumerate(m):
            if crate: stacks[i+1].insert(0, crate)
    
    moves = []
    for row in day_input:
        m = re.match(r'^move (\d+) from (\d+) to (\d+)$', row)
        if not m: continue
        n, s, e = map(int, m.groups())
        # print('Move', n, 'from', s, 'to', e)
        moves.append((n, s, e))

    p1_stacks = copy.deepcopy(stacks)
    for n, s, e in moves:
        for _ in range(n): p1_stacks[e].append(p1_stacks[s].pop())

    p2_stacks = copy.deepcopy(stacks)
    for n, s, e in moves:
        p2_stacks[e] += p2_stacks[s][-n:]
        p2_stacks[s] = p2_stacks[s][:-n] 

    return format(p1_stacks), format(p2_stacks)
