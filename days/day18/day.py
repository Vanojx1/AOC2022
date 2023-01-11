import matplotlib.pyplot as plt
import numpy as np

class Cube(object):
    def __init__(self, x, y, z) -> None:
        self.x, self.y, self.z = x, y, z

    @property
    def faces(self):
        return set([
            Cube(self.x+1, self.y, self.z),
            Cube(self.x-1, self.y, self.z),
            Cube(self.x, self.y+1, self.z),
            Cube(self.x, self.y-1, self.z),
            Cube(self.x, self.y, self.z+1),
            Cube(self.x, self.y, self.z-1)
        ])

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    def __eq__(self, o) -> bool:
        return hash(self) == hash(o)
    def __repr__(self) -> str:
        return f'C({self.x}, {self.y}, {self.z})'

def main(day_input):

    SHOW_PLOT = 0

    cubes = set([Cube(*map(int, row.split(','))) for row in day_input])

    def count_faces(air=set([])):
        for cube in cubes:
            yield len(cube.faces - cubes - air)

    minx, maxx = min(cubes, key=lambda c: c.x).x, max(cubes, key=lambda c: c.x).x
    miny, maxy = min(cubes, key=lambda c: c.y).y, max(cubes, key=lambda c: c.y).y
    minz, maxz = min(cubes, key=lambda c: c.z).z, max(cubes, key=lambda c: c.z).z

    around_list = set([f for cube in cubes for f in cube.faces]) - cubes
    full_space = around_list | cubes

    total_air = set([])

    def expand(cube):
        q = [cube]
        visited = set([cube])
        while q:
            curr_cube = q.pop()
            for f in curr_cube.faces:
                if f in cubes or f in total_air: continue
                if not (minx <= f.x <= maxx and miny <= f.y <= maxy and minz <= f.z <= maxz): return False
                if f not in visited:
                    visited.add(f)
                    q.append(f)
        return visited

    for cube in around_list:
        if air := expand(cube):
            total_air |= air

    if SHOW_PLOT:
        maxt = max(maxx, maxy, maxz)+10
        x, y, z = np.indices((maxt, maxt, maxt))
        k = [((x == c.x) & (y == c.y) & (z == c.z)) for c in full_space]
        voxelarray = k[0]
        for c in k[1:]: voxelarray |= c
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, edgecolor='k')
        plt.show()

    return sum(count_faces()), sum(count_faces(total_air))