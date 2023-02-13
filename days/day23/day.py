from utils import Point
from collections import defaultdict

def main(day_input):

    N, NE, E, SE, S, SW, W, NW = (-1j, 1-1j, 1, 1+1j, 1j, -1+1j, -1, -1-1j)

    class Grove:

        def __init__(self) -> None:
            self.elf_map = {Point(x, y) for y, row in enumerate(day_input) for x, v in enumerate(row) if v == '#'}
            self.x_coords = list(map(lambda p: p.x, self.elf_map))
            self.y_coords = list(map(lambda p: p.y, self.elf_map))
            self.dir_list = [(self.go_north, N), (self.go_south, S), (self.go_west, W), (self.go_east, E)]

        def go_nope(self, elf):
            return all(elf+o not in self.elf_map for o in (N, NE, E, SE, S, SW, W, NW))

        def go_north(self, elf):
            return all(elf+o not in self.elf_map for o in (N, NE, NW))

        def go_south(self, elf):
            return all(elf+o not in self.elf_map for o in (S, SE, SW))

        def go_west(self, elf):
            return all(elf+o not in self.elf_map for o in (W, NW, SW))
        
        def go_east(self, elf):
            return all(elf+o not in self.elf_map for o in (E, NE, SE))

        def take_turn(self):
            moves = defaultdict(list)
            removed = set([])
            for elf in self.elf_map:
                if self.go_nope(elf): continue
                for dir_fn, d in self.dir_list:
                    if dir_fn(elf):
                        moves[elf+d].append(elf)
                        break
            
            self.dir_list.append(self.dir_list.pop(0))

            for new_elf, elfs in moves.items():
                if len(elfs) == 1:
                    self.elf_map.remove(elfs[0])
                    self.x_coords.remove(elfs[0].x)
                    self.y_coords.remove(elfs[0].y)
                    removed.add(elfs[0])
                    self.elf_map.add(new_elf) 
                    self.x_coords.append(new_elf.x)
                    self.y_coords.append(new_elf.y)
            
            return removed
        
        def print(self, removed=set([])):
            for y in range(self.ymin, self.ymax+1):
                for x in range(self.xmin, self.xmax+1):
                    if Point(x, y) in removed:
                        print('o', end='')
                    else:
                        print('#' if Point(x, y) in self.elf_map else '.', end='')
                print()
            print()

        @property
        def xmin(self): return min(self.x_coords)
        @property
        def xmax(self): return max(self.x_coords)
        @property
        def ymin(self): return min(self.y_coords)
        @property
        def ymax(self): return max(self.y_coords)
        @property
        def empty_ground(self):
            return (self.xmax-self.xmin+1)*(self.ymax-self.ymin+1)-len(self.elf_map)

    grove = Grove()
    t10_empty_ground = None
    turn = 1
    while True:
        removed = grove.take_turn()
        if turn == 10: t10_empty_ground = grove.empty_ground
        if len(removed) == 0: break
        turn += 1

    return t10_empty_ground, turn