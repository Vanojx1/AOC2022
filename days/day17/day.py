from itertools import cycle
from utils import Point

class Rock:

    RIGHTWALL = 6

    def __init__(self, shape, miny) -> None:
        if shape == '-':
            self.parts = set([Point(2, miny-3), Point(3, miny-3), Point(4, miny-3), Point(5, miny-3)])
        elif shape == '+':
            self.parts = set([Point(3, miny-5), Point(2, miny-4), Point(3, miny-4), Point(4, miny-4), Point(3, miny-3)])
        elif shape == 'L':
            self.parts = set([Point(4, miny-5), Point(4, miny-4), Point(2, miny-3), Point(3, miny-3), Point(4, miny-3)])
        elif shape == 'I':
            self.parts = set([Point(2, miny-6), Point(2, miny-5), Point(2, miny-4), Point(2, miny-3)])
        elif shape == 'O':
            self.parts = set([Point(2, miny-4), Point(3, miny-4), Point(2, miny-3), Point(3, miny-3)])

        self.start_miny = miny

    @property
    def dy(self):
        return self.miny - self.start_miny
    @property
    def minx(self):
        return min(self.parts, key=lambda p: p.x).x
    @property
    def maxx(self):
        return max(self.parts, key=lambda p: p.x).x
    @property
    def miny(self):
        return min(self.parts, key=lambda p: p.y).y
    @property
    def maxy(self):
        return max(self.parts, key=lambda p: p.y).y

    def push(self, d, cave):
        new_parts = None
        if d == '>' and self.maxx < self.RIGHTWALL:
            new_parts = set([p+1 for p in self.parts])
        elif d == '<' and self.minx > 0:
            new_parts = set([p-1 for p in self.parts])
        elif d == 'v' and self.maxy < 0:
            new_parts = set([p+1j for p in self.parts])
        
        if new_parts and not (new_parts & cave):
            self.parts = new_parts
            return True, None, None

        if d in '<>': return True, None, None

        return False, min(self.start_miny, self.miny-1), cave | self.parts

def main(day_input):
    jet_l = len(day_input[0])

    def drop(N=None):
        jet_of_gas = cycle(day_input[0])
        rockseq = cycle(['-', '+', 'L', 'I', 'O'])
        cave = set([])
        miny = 0
        rock_n = 0
        jet_n = 0
        states = []
        while True:
            r = Rock(next(rockseq), miny)
            while True:
                r.push(next(jet_of_gas), cave)
                jet_n += 1
                k, new_miny, new_cave = r.push('v', cave)
                if not k:
                    miny = new_miny
                    cave = new_cave
                    break

            state = tuple([r.minx, r.maxx, r.dy, miny-r.maxy, rock_n % 5, jet_n % jet_l])
            states.append(state)
            if N is None:
                prev = [i for i, p in enumerate(states) if p == state]
                if len(prev) >= 3: return abs(miny), prev
            elif rock_n == N-1: return abs(miny), []

            rock_n += 1

    y_2022, _ = drop(2022)

    _, repeat = drop()

    start = repeat[0] + repeat[1]
    delta = repeat[2] - repeat[1]

    y0, _ = drop(start)
    y1, _ = drop(start + delta)
    y1 -= y0

    N = 1000000000000
    delta_in_N = (N-start) // delta
    rem = (N-start) % delta

    y2, _ = drop(start+delta+rem)
    y2 -= y0 + y1

    return y_2022, y0 + delta_in_N*y1 + y2   

    