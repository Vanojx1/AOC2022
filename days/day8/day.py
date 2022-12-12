from termcolor import colored
from functools import reduce

class Tree:
    forest_w = 0
    forest_h = 0
    forest = None
    def __init__(self, x, y, h) -> None:
        self.x = x
        self.y = y
        self.h = h
    
    def iter(self):
        l, r, u, d = [], [], [], []
        for x in range(self.x+1, self.forest_w+1):
            coord = (x, self.y)
            r.append(coord)
            if self.forest[coord] >= self.h: break
        for bx in range(self.x-1, -1, -1):
            coord = (bx, self.y)
            l.append(coord)
            if self.forest[coord] >= self.h: break
        for y in range(self.y+1, self.forest_h+1):
            coord = (self.x, y)
            d.append(coord)
            if self.forest[coord] >= self.h: break
        for by in range(self.y-1, -1, -1):
            coord = (self.x, by)
            u.append(coord)
            if self.forest[coord] >= self.h: break
        return (u, l, d, r)
    
    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def scenic_score(self):
        return reduce(lambda n,c: n*len(c), self.iter(), 1)

def main(day_input):
    forest = {(x, y): int(h) for y, row in enumerate(day_input) for x, h in enumerate(row)}
    
    visible_trees = set([])
    forest_w, forest_h = max(forest.keys())

    Tree.forest_w = forest_w
    Tree.forest_h = forest_h
    Tree.forest = forest

    for y in range(forest_h+1):
        rmax = rbmax = -1
        for x in range(forest_w+1):
            bx = forest_w-x
            if forest[(x, y)] > rmax:
                visible_trees.add((x, y))
                rmax = forest[(x, y)]
            if forest[(bx, y)] > rbmax:
                visible_trees.add((bx, y))
                rbmax = forest[(bx, y)]
    for x in range(forest_w+1):
        cmax = cbmax = -1
        for y in range(forest_h+1):
            by = forest_h-y
            if forest[(x, y)] > cmax:
                visible_trees.add((x, y))
                cmax = forest[(x, y)]
            if forest[(x, by)] > cbmax:
                visible_trees.add((x, by))
                cbmax = forest[(x, by)]

    trees = [Tree(x, y, h) for (x, y), h in forest.items()]
    best_tree = max(trees, key=lambda t: t.scenic_score)
    best_tree_visibles = reduce(lambda n,c: n+c, best_tree.iter(), [])
    
    # for t in trees: print(t.pos, t.h, t.iter(), t.scenic_score)

    for y in range(forest_h+1):
        for x in range(forest_w+1):
            if (x, y) == best_tree.pos:
                print(colored(forest[(x, y)], 'red'), end='')
            elif (x, y) in best_tree_visibles:
                print(colored(forest[(x, y)], 'blue'), end='')
            elif (x, y) in visible_trees:
                print(colored(forest[(x, y)], 'green'), end='')
            else:
                print(forest[(x, y)], end='')
        print()

    return len(visible_trees), best_tree.scenic_score