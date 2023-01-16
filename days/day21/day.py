import re
from operator import mul, sub, add, floordiv
from sympy import sympify, solve, Symbol

op_mapping = {'*': mul, '-': sub, '+': add, '/': floordiv}

class Jobs(dict):
    
    def __getitem__(self, key):
        v = super().__getitem__(key)
        if isinstance(v, int): return v
        m1, op, m2 = v
        return op_mapping[op](self[m1], self[m2])
    
    def get_raw(self, key):
        return super().__getitem__(key)
    
    def as_path(self, key):
        v = super().__getitem__(key)
        if isinstance(v, int): return set([])
        m1, _, m2 = v
        return set([m1, m2]) | self.as_path(m1) | self.as_path(m2)
    
    def as_equation(self, key):
        v = super().__getitem__(key)
        if key == 'humn': return 'x'
        if isinstance(v, int): return v
        m1, op, m2 = v
        return f'({self.as_equation(m1)}{op}{self.as_equation(m2)})'


def main(day_input):
    jobs = Jobs()

    for row in day_input:
        m = re.match(r'^(\w+): (?:(?:(\w+) ([+-\/*]) (\w+))|(\d+))', row).groups()
        monkey, m1, op, m2, n = m

        if n is not None:
            jobs[monkey] = int(n)
        else:
            jobs[monkey] = (m1, op, m2)

    for key in list(jobs.keys()):
        if 'humn' not in jobs.as_path(key):
            jobs[key] = jobs[key]

    m1, op, m2 = jobs.get_raw('root')
    eq = sympify(f"Eq({jobs.as_equation(m1)}, {jobs[m2]})")
    eq_solution, = solve(eq, Symbol('x'))

    return jobs['root'], eq_solution