import re, os, time
from termcolor import colored

def main(day_input):
    rocks = set([])
    for row in day_input:
        curr_pos, *steps = list(map(lambda xy: complex(*map(int, xy.split(','))), re.findall(r'(\d+,\d+)', row)))
        rocks.add(curr_pos)
        for step in steps:
            d = step-curr_pos
            if d.real == 0:
                off = 1 if step.imag-curr_pos.imag > 0 else -1
                for y in range(int(curr_pos.imag), int(step.imag)+off, off):
                    rocks.add(complex(curr_pos.real, y))
            else:
                off = 1 if step.real-curr_pos.real > 0 else -1
                for x in range(int(curr_pos.real), int(step.real)+off, off):
                    rocks.add(complex(x, curr_pos.imag))
            curr_pos = step

    ymin, ymax = 0, int(max(r.imag for r in rocks))
    xmin, xmax = int(min(r.real for r in rocks)), int(max(r.real for r in rocks))
    SOURCE = complex(500, 0)
    FLOOR = ymax+2

    sand = set([])

    def print_cave():
        os.system('cls')
        print()
        for y in range(FLOOR-ymin+1):
            for x in range(xmax-xmin+3):
                curr_pos = complex(xmin+x-1, ymin+y)
                if curr_pos in sand:
                    print(colored('o', 'yellow'), end='')
                elif curr_pos == SOURCE:
                    print(colored('+', 'red'), end='')
                elif curr_pos in rocks or y == FLOOR:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()
        time.sleep(0.05)

    sand_under_rock = None
    def drop():
        nonlocal xmin, xmax, sand_under_rock
        curr_pos = complex(500, 0)
        floor = set([complex(x, FLOOR) for x in range(xmin-2, xmax+3)])
        full_map = rocks | sand | floor
        d = 1j
        dl = -1+1j
        dr = 1+1j
        while True:
            if curr_pos+d not in full_map: curr_pos+=d
            elif curr_pos+dl not in full_map: curr_pos+=dl
            elif curr_pos+dr not in full_map: curr_pos+=dr
            else: break
        if curr_pos.imag > ymax and sand_under_rock is None: sand_under_rock = len(sand)
        sand.add(curr_pos)
        if curr_pos.real < xmin: xmin = int(curr_pos.real)
        if curr_pos.real > xmax: xmax = int(curr_pos.real)
        if curr_pos == SOURCE: return False
        return True
    
    while drop(): pass # print_cave()

    return sand_under_rock, len(sand)