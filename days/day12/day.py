import heapq
from termcolor import colored
import math

class Point(complex):
    def __lt__(self, o):
        return self.real < o.real or self.imag < o.imag
    def __add__(self, o) -> 'Point':
        r = super().__add__(o)
        return Point(r.real, r.imag) 

def d(a, b): return math.sqrt((a.real-b.real)**2+(a.imag-b.imag)**2)

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

    def print_map(path1, path2):
        print()
        def get_char(path, cpos):
            i = path.index(cpos)
            try: diff = path[i+1]-cpos
            except IndexError: diff = end-cpos
            try: return arrows[diff]
            except KeyError: return '#'
        for y in range(ymax+1):
            row=''
            for x in range(xmax+1):
                cpos = Point(x, y)
                if cpos in path1:
                    row += colored(get_char(path1, cpos), 'green')
                elif cpos in path2:
                    row += colored(get_char(path2, cpos), 'red')
                else:
                    row += heightmap[cpos]
            print(row)
        print()

    def walk(current_start):
        q = [(0, d(current_start, end), [current_start])]
        heapq.heapify(q)
        visited = set([])
        while q:
            _, _, path = heapq.heappop(q)
            
            pos = path[-1]

            if pos == end:
                return path

            for next_pos in [pos+off for off in (-1j, 1, 1j, -1)]:
                if next_pos in heightmap and next_pos not in visited and (ord(heightmap[next_pos])-ord(heightmap[pos])) <= 1:
                    heapq.heappush(q, (len(path)+1, d(next_pos, end), path + [next_pos]))
                    visited.add(next_pos)

    path = walk(start)
    min_path = min([walk(s) for s, h in heightmap.items() if h == 'a'], key=lambda p: len(p) if p else float('inf'))

    print_map(min_path, path)

    return len(path)-1, len(min_path)-1