from math import sqrt

def d(a, b): return sqrt((a.real-b.real)**2+(a.imag-b.imag)**2)

class Rope:
    
    DIRS = { 'U': -1j, 'D': 1j, 'L': -1, 'R': 1}

    def __init__(self, length, parent=None) -> None:
        self.pos = 0j
        self.pos_history = set([0j])
        self.parent = parent
        if not parent: self.label = 'H'
        elif length > 1: self.label = str(length-1)
        else: self.label = 'T'
        self.next = Rope(length-1, self) if length > 1 else None
    
    @property
    def is_head(self):
        return self.parent is None
    
    @property
    def is_tail(self):
        return self.next is None

    def move(self, dir):
        if self.is_head:
            self.pos += self.DIRS[dir]
        elif self.pos not in self.around_parent:
            self.pos = self.next_pos
        if self.is_tail: return self.pos
        return self.next.move(dir)

    @property
    def next_pos(self):
        return sorted([self.pos+o for o in (-1j, 1-1j, 1, 1+1j, 1j, -1+1j, -1, -1-1j)], key=lambda x: d(self.parent.pos, x))[0]

    @property
    def around_parent(self):
        return [self.parent.pos+o for o in (0, -1j, 1-1j, 1, 1+1j, 1j, -1+1j, -1, -1-1j)]

def main(day_input):

    moves = [[fn(v) for fn, v in zip([str, int], r.split(' '))] for r in day_input]
    
    rope2 = Rope(2)
    rope2_history = set([rope2.pos])
    for dir, steps in moves:
        for _ in range(steps):
            rope2_history.add(rope2.move(dir))

    rope10 = Rope(10)
    rope10_history = set([rope10.pos])
    for dir, steps in moves:
        for _ in range(steps):
            rope10_history.add(rope10.move(dir))

    return len(rope2_history), len(rope10_history)
