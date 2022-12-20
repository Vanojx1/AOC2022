import json
from functools import cmp_to_key

NoneType = type(None)

def compare(l1, l2):
    m = max(len(l1), len(l2))
    for el1, el2 in zip(l1 + [None] * (m-len(l1)), l2 + [None] * (m-len(l2))):
        t = (type(el1), type(el2))
        r = None
        if t == (int, int):
            if el1 == el2: continue
            if el1 < el2: r = -1
            elif el1 > el2: r = 1
            else: r = 0
        elif t == (list, int):
            r = compare(el1, [el2])
        elif t == (int, list):
            r = compare([el1], el2)
        elif t == (list, list):
            r = compare(el1, el2)
        elif t in ((NoneType, int), (NoneType, list)):
            return -1
        elif t in ((int, NoneType), (list, NoneType)):
            return 1
        if r is not None: return r

def main(day_input):
    pairs = []
    for row in day_input:
        if not row: continue
        row = json.loads(row)
        if not pairs or len(pairs[-1]) == 2: pairs.append((row,))
        elif len(pairs[-1]) == 1: pairs[-1] = (pairs[-1][0], row)

    def gen_indexes():
        for i, p in enumerate(pairs):
            if compare(*p) == -1: yield i+1

    div1 = [[2]]
    div2 = [[6]]

    sorted_packets = sorted([el for pair in pairs for el in pair] + [div1, div2], key=cmp_to_key(compare))

    return sum(gen_indexes()), (sorted_packets.index(div1)+1) * (sorted_packets.index(div2)+1)