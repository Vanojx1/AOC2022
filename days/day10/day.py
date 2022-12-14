import re
from termcolor import colored

class CPU:
    def __init__(self) -> None:
        self.cycle = 0
        self.op_index = 0
        self.reg_value = 1
        self.program = []

        self.breakpoints = []
        self.values_at = []
        self.ctr_screen = ['']

    def set_breakpoints(self, brp):
        self.breakpoints = brp

    def load(self, program):
        self.program = program

    def exec(self):
        op, param = self.program[self.op_index]
        yield from getattr(self, op)(param)
        self.op_index += 1
        self.op_index %= len(self.program)
    def noop(self, n):
        yield 1
    def addx(self, n):
        yield 1
        self.reg_value += n
        yield 1

    @property
    def sprite_pos(self):
        row = (self.cycle-1) // 40
        return [(40*row)+self.reg_value+offset for offset in (-1, 0, 1)]

    def run(self, cycles):
        l = self.exec()
        while True:
            self.cycle += 1
            if self.cycle in self.breakpoints: self.values_at.append(self.reg_value)
            self.ctr_screen[-1] += '#' if self.cycle-1 in self.sprite_pos else '.'
            if len(self.ctr_screen[-1]) == 40: self.ctr_screen.append('')

            try:
                next(l)
            except StopIteration:
                l = self.exec()
                next(l)
            if self.cycle == cycles: break

def parse_op(raw):
    m = re.match(r'(noop|addx)(?: (-?\d+))?', raw)
    return m.group(1), int(m.group(2)) if m.group(2) else None

def main(day_input):

    cpu = CPU()
    cpu.load([parse_op(raw_op) for raw_op in day_input])
    cpu.set_breakpoints([20, 60, 100, 140, 180, 220])
    cpu.run(240)

    print()
    [([print('🟥' if c == '#' else '⬜️', end='') for c in row], print()) for row in cpu.ctr_screen]

    return sum([b*v for b, v in zip(cpu.breakpoints, cpu.values_at)]), 'PAPKFKEJ' # <--- Manually set ofc...
