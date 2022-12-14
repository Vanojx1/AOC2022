import re
from collections import OrderedDict
from math import lcm
from functools import reduce

class Item:
    index = 0
    mod_lcm = None
    OPS = {'+': lambda a, b: a+b, '*': lambda a, b: a*b, '/': lambda a, b: a//3}

    def __init__(self, value) -> None:
        self.id = Item.index
        Item.index += 1
        self.value = int(value)
    def apply(self, op):
        self.value = self.OPS[op[0]](self.value, self.value if op[1] == 'old' else int(op[1])) % self.mod_lcm
    
    @property
    def real_value(self):
        return self.value

class Monkey:
    def __init__(self, id, items, op, test, throw_true, throw_false) -> None:
        self.id = id
        self.items = items
        self.op = op
        self.test = test
        self.throw_true = throw_true
        self.throw_false = throw_false
        self.throws = 0
    
    def calc_throw(self, divide):
        item = self.items[0]
        item.apply(self.op)
        if divide: item.apply(('/', 3))
        return self.throw_true if item.real_value % self.test == 0 else self.throw_false
    
    def take_turn(self, divide=True):
        while len(self.items) > 0:
            target = self.calc_throw(divide)
            self.monkey_map[target].items.append(self.items.pop(0))
            self.throws += 1

def main(day_input):
    day_input_full = '\n'.join(day_input)
    m = re.findall(r'^Monkey (\d):\n  Starting items: ((?:\d+(?:, )?)+)\n  Operation: new = old ([+*]) (\d+|old)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)$', day_input_full, re.MULTILINE)

    def gen_monkeys():
        monkeys = OrderedDict()
        for row in m:
            id, items, op1, op2, test, throw_true, throw_false = row
            monkeys[int(id)] = Monkey(int(id), [Item(i) for i in items.split(', ')], (op1, op2), int(test), int(throw_true), int(throw_false))
        return monkeys
    
    Item.index = 0
    monkeys = gen_monkeys()
    Monkey.monkey_map = monkeys
    Item.mod_lcm = reduce(lcm, [m.test for m in monkeys.values()])

    for _ in range(20): [m.take_turn() for m in monkeys.values()]
    p1m1, p1m2 = sorted(monkeys.values(), key=lambda m: m.throws, reverse=True)[:2]

    Item.index = 0
    monkeys = gen_monkeys()
    Monkey.monkey_map = monkeys

    for _ in range(10000): [m.take_turn(False) for m in monkeys.values()]
    p2m1, p2m2 = sorted(monkeys.values(), key=lambda m: m.throws, reverse=True)[:2]

    return p1m1.throws*p1m2.throws, p2m1.throws*p2m2.throws
