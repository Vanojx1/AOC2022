import heapq
from termcolor import colored

class Point(complex):
    def __lt__(self, o):
        return self.real < o.real or self.imag < o.imag
    def __add__(self, o) -> 'Point':
        r = super().__add__(o)
        return Point(r.real, r.imag) 

def d(a, b): return abs(a.real-b.real)+abs(a.imag-b.imag)

def main(day_input):
    heightmap = {Point(x, y): h for y, row in enumerate(day_input) for x, h in enumerate(row)}

    for k, v in heightmap.items():
        if v == 'S':
            start = k
            heightmap[k] = 'a'
        if v == 'E': 
            end = k
            heightmap[k] = 'z'

    xmax, ymax = int(max([m.real for m in heightmap.keys()])), int(max([m.imag for m in heightmap.keys()]))

    arrows = {-1: '<',1: '>',1j: 'v',-1j: '^',0j: 'X'}

    print(start, end)
    print(xmax, ymax)

    def print_map(path):
        for y in range(ymax+1):
            row=''
            for x in range(xmax+1):
                cpos = Point(x, y)
                if cpos in path:
                    i = path.index(cpos)
                    try: diff = path[i+1]-cpos
                    except IndexError: diff = end-cpos
                    # print(arrows[diff], end='')
                    row += arrows[diff]
                else:
                    row += ' ' 
                    # print('⬜️', end='')
            print(row)
        print()

    def walk():
        q = [(d(start, end), [start])]
        heapq.heapify(q)
        visited = set([])
        while q:
            _, path = heapq.heappop(q)
            
            pos = path[-1]

            # print('==>', pos)

            if pos == end:
                print('Found!', len(path)-1)
                return path

            for next_pos in [pos+off for off in (-1j, 1, 1j, -1)]:
                if next_pos in heightmap and next_pos not in visited and abs(ord(heightmap[next_pos])-ord(heightmap[pos])) < 2:
                    heapq.heappush(q, (d(next_pos, end), path + [next_pos]))
                    visited.add(next_pos)

    path = walk()

    print_map(path)

    return None, None