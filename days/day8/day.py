from termcolor import colored

def main(day_input):
    forest = {(x, y): int(h) for y, row in enumerate(day_input) for x, h in enumerate(row)}
    
    visible_trees = set([])
    forest_w, forest_h = max(forest.keys())

    for y in range(forest_h+1):
        row_max = -1
        for x in range(forest_w+1):
            if forest[(x, y)] > row_max:
                visible_trees.add((x, y))
                row_max = forest[(x, y)]
        row_max = -1
        for x in range(forest_w, -1, -1):
            if forest[(x, y)] > row_max:
                visible_trees.add((x, y))
                row_max = forest[(x, y)]
    
    for x in range(forest_w+1):
        col_max = -1
        for y in range(forest_h+1):
            if forest[(x, y)] > col_max:
                visible_trees.add((x, y))
                col_max = forest[(x, y)]
        col_max = -1
        for y in range(forest_h, -1, -1):
            if forest[(x, y)] > col_max:
                visible_trees.add((x, y))
                col_max = forest[(x, y)]

    for y in range(forest_h+1):
        for x in range(forest_w+1):
            print(colored(forest[(x, y)], 'green') if (x, y) in visible_trees else forest[(x, y)], end='')
        print()

    return len(visible_trees), None