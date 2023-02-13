from utils import Point
from collections import defaultdict, deque, OrderedDict
import re
import heapq
import numpy as np

def main(day_input):

    # STEP 1
    #
    # mapping walls and jungle
    # row_min_max and col_min_max map coords for part 1 rotations
    # 
    walls, jungle_map = set([]), set([])
    row_min_max = defaultdict(lambda: (float('inf'), 0))
    col_min_max = defaultdict(lambda: (float('inf'), 0))
    for y, row in enumerate(day_input[:-2]):
        for x, v in enumerate(row):
            if v not in '#.': continue
            if v == '#': walls.add(Point(x, y))
            if v == '.': jungle_map.add(Point(x, y))
            row_min_max[y] = (min(row_min_max[y][0], x-1), max(row_min_max[y][1], x+1))
            col_min_max[x] = (min(col_min_max[x][0], y-1), max(col_min_max[x][1], y+1))

    # STEP 2
    #
    # Finding face size, very slow but...
    #
    full_points = jungle_map | walls
    xmin, xmax = min(map(lambda p: p.x, full_points)), max(map(lambda p: p.x, full_points))
    ymin, ymax = min(map(lambda p: p.y, full_points)), max(map(lambda p: p.y, full_points))

    FACE_SIZE = float('inf')
    for y in range(ymin, ymax+1):
        rmin, rmax = min([p.x for p in full_points if p.y == y]), max([p.x for p in full_points if p.y == y])
        FACE_SIZE = min(FACE_SIZE, rmax-rmin+1)

    # STEP 3
    #
    # Finding face --> coord association
    # using matrix rotation and BFS
    #
    matrix = np.arange(27).reshape((3, 3, 3))

    r_up    = (1, 0)
    r_down  = (0, 1)
    r_right = (1, 2)
    r_left  = (2, 1)

    top     = matrix[:,0,:]
    bottom  = matrix[:,2,:]
    front   = matrix[0,:,:]
    back    = matrix[2,:,:]
    left    = matrix[:,:,0]
    right   = matrix[:,:,2]

    faces = {
        tuple(sorted(top.flatten())):   'TOP',
        tuple(sorted(bottom.flatten())):'BOTTOM',
        tuple(sorted(front.flatten())): 'FRONT',
        tuple(sorted(back.flatten())):  'BACK',
        tuple(sorted(left.flatten())):  'LEFT',
        tuple(sorted(right.flatten())): 'RIGHT'
    }

    corners = set([])    
    start_face = 'TOP'
    face_to_coord = {}
    start_matrix = matrix.copy()
    q = [(min(jungle_map), [start_face], [], start_matrix)]
    while q:

        curr, face_path, path, curr_matrix = q.pop()

        corners.add(curr)
        face_to_coord[face_path[-1]] = curr

        for n, d, rot in zip([curr+o for o in (Point(0, -FACE_SIZE), Point(FACE_SIZE, 0), Point(0, FACE_SIZE), Point(-FACE_SIZE, 0))], ['U', 'R', 'D', 'L'], [r_up, r_right, r_down, r_left]):
            if n not in corners and n in (jungle_map | walls):
                next_matrix = np.rot90(curr_matrix, k=1, axes=rot)
                nf = faces[tuple(sorted(next_matrix[:,0,:].flatten()))]
                corners.add(n)
                q.append((n, face_path + [nf], path + [d], next_matrix))
    
    abs_faces = {}
    for face, coord in face_to_coord.items():
        abs_faces[face] = Point((coord.x-face_to_coord[start_face].x)//FACE_SIZE, (coord.y-face_to_coord[start_face].y)//FACE_SIZE)
    abs_coords = {coord: face for face, coord in abs_faces.items()}
    
    # STEP 4
    #
    # Define CubeFace class
    # store original coords, reduced coords and faces connections
    #
    opposite = {'U': 'D', 'D': 'U', 'R': 'L', 'L': 'R'}
    class CubeFace:

        def __init__(self, label, abs_coord, real_coord) -> None:
            self.label = label
            self.abs_coord = coord
            self.real_coord = real_coord
            self.connections = OrderedDict({'U': None, 'R': None, 'D': None, 'L': None})
            self.jungle_map = {self.real_coord + complex(x, y) for y in range(FACE_SIZE) for x in range(FACE_SIZE)}
            self.minx, self.maxx = min(map(lambda p: p.x, self.jungle_map)), max(map(lambda p: p.x, self.jungle_map))
            self.miny, self.maxy = min(map(lambda p: p.y, self.jungle_map)), max(map(lambda p: p.y, self.jungle_map))

            for n, d in zip([self.abs_coord+o for o in (-1j, 1, 1j, -1)], ['U', 'R', 'D', 'L']):
                if n in abs_coords:
                    self.connections[d] = (abs_coords[n], opposite[d])

        @property
        def transitions(self):
            return [
                ('U', *self.connections['U']),
                ('R', *self.connections['R']),
                ('D', *self.connections['D']),
                ('L', *self.connections['L'])
            ]

        def dx(self, cp): return cp.x-self.minx
        def dxb(self, cp): return self.maxx-cp.x
        def dy(self, cp): return cp.y-self.miny
        def dyb(self, cp): return self.maxy-cp.y
        
        @property
        def av_faces(self):
            for (k, v), o in zip(self.connections.items(), (-1j, 1, 1j, -1)):
                if v is None:
                    yield k, self.abs_coord+o 

    cube_faces = {}
    for face, coord in abs_faces.items():
        cf = CubeFace(face, coord, face_to_coord[face])
        cube_faces[face] = cf

    # STEP 5
    #
    # Finding faces connections
    # repeating BFS increasing max distance
    # with diff face, diff face x, diff face y as constraint
    # 
    def get_av_pos():
        def _():
            for face, cf in cube_faces.items():
                for d, p in cf.av_faces:
                    yield (face, d, p)
        return list(_())

    def face_to_face(p1, p2, max_s, used):
        q = [(0, p1.mdist(p2), p1, [p1])]
        heapq.heapify(q)
        curr_used = set([p1, *used])

        while q:
            steps, _, curr_pos, path = heapq.heappop(q)
            if curr_pos == p2: return set(path)
            for n in [curr_pos+o for o in (-1j, 1, 1j, -1)]:
                if n not in curr_used and steps+1 <= max_s:
                    curr_used.add(n)
                    heapq.heappush(q, (steps+1, n.mdist(p2), n, path + [n]))

    used = set(abs_faces.values())
    for max_s in range(15):
        av_pos = get_av_pos()
        if not av_pos: break
        for f1, d1, p1 in av_pos:
            av_pos = get_av_pos()
            for f2, d2, p2 in av_pos:
                if f1 == f2 or abs_faces[f1].y == abs_faces[f2].y or abs_faces[f1].x == abs_faces[f2].x: continue
                new_used = face_to_face(p1, p2, max_s, used)
                if new_used is not None:
                    used |= new_used
                    cube_faces[f1].connections[d1] = (f2, d2)
                    cube_faces[f2].connections[d2] = (f1, d1)
    
    # just a transition map
    # (from face, to face): (current face, new face, current position) => new position
    transitions_map = {
        ('U', 'U'): lambda cf, nf, cp: Point(nf.maxx-cf.dx(cp), nf.miny),
        ('U', 'R'): lambda cf, nf, cp: Point(nf.maxx, nf.maxy-cf.dx(cp)),
        ('U', 'D'): lambda cf, nf, cp: Point(nf.minx+cf.dx(cp), nf.maxy),
        ('U', 'L'): lambda cf, nf, cp: Point(nf.minx, nf.miny+cf.dx(cp)),

        ('R', 'U'): lambda cf, nf, cp: Point(nf.minx+cf.dyb(cp), nf.miny),
        ('R', 'R'): lambda cf, nf, cp: Point(nf.maxx, nf.miny+cf.dyb(cp)),
        ('R', 'D'): lambda cf, nf, cp: Point(nf.minx+cf.dy(cp), nf.maxy),
        ('R', 'L'): lambda cf, nf, cp: Point(nf.minx, nf.miny+cf.dy(cp)),

        ('D', 'U'): lambda cf, nf, cp: Point(nf.minx+cf.dx(cp), nf.miny),
        ('D', 'R'): lambda cf, nf, cp: Point(nf.maxx, nf.miny+cf.dx(cp)),
        ('D', 'D'): lambda cf, nf, cp: Point(nf.minx+cf.dxb(cp), nf.maxy),
        ('D', 'L'): lambda cf, nf, cp: Point(nf.minx, nf.miny+cf.dxb(cp)),

        ('L', 'U'): lambda cf, nf, cp: Point(nf.minx+cf.dy(cp), nf.miny),
        ('L', 'R'): lambda cf, nf, cp: Point(nf.maxx, nf.miny+cf.dy(cp)),
        ('L', 'D'): lambda cf, nf, cp: Point(nf.minx+cf.dyb(cp), nf.maxy),
        ('L', 'L'): lambda cf, nf, cp: Point(nf.minx, nf.miny+cf.dyb(cp)),
        
    }

    # STEP 6
    #
    # Walk over the map/cube
    #
    def walk(trans_fn):
        steps = re.findall(r'\d+|[R,L]', day_input[-1])
        dir_list = [1, 1j, -1, -1j]
        dirs = deque(dir_list)
        arrows = {1: '>', 1j: 'v', -1: '<', -1j: '^'}
        curr_dir = dirs[0]
        curr_pos = min(jungle_map)
        dir_map = {'R': lambda: dirs.rotate(-1), 'L': lambda: dirs.rotate(1)}
        curr_face = cube_faces['TOP']

        def dirs_go_to(new_dir):
            while dirs[0] != new_dir: dirs.rotate(-1)
        
        for step in steps:
            if step in 'RL':
                dir_map[step]()
                curr_dir = dirs[0]
            else:
                for _ in range(int(step)):
                    next_pos = curr_pos + curr_dir
                    next_face, next_dir, next_pos = trans_fn(curr_face, curr_dir, curr_pos, next_pos)
                    if next_pos in walls: break
                    curr_face, curr_dir = next_face, next_dir
                    dirs_go_to(curr_dir)
                    curr_pos = next_pos

        return curr_pos.x+1, curr_pos.y+1, dir_list.index(curr_dir)

    def transition_fn_2D(curr_face, curr_dir, curr_pos, next_pos):
        if curr_dir in (1, -1) and next_pos.x in row_min_max[next_pos.y]:
            if row_min_max[next_pos.y].index(next_pos.x) == 0:
                return curr_face, curr_dir, Point(row_min_max[next_pos.y][1]-1, next_pos.y)
            else:
                return curr_face, curr_dir, Point(row_min_max[next_pos.y][0]+1, next_pos.y)
        elif curr_dir in (1j, -1j) and next_pos.y in col_min_max[next_pos.x]:
            if col_min_max[next_pos.x].index(next_pos.y) == 0:
                return curr_face, curr_dir, Point(next_pos.x, col_min_max[next_pos.x][1]-1)
            else:
                return curr_face, curr_dir, Point(next_pos.x, col_min_max[next_pos.x][0]+1)
        return curr_face, curr_dir, next_pos

    def transition_fn_3D(curr_face, curr_dir, curr_pos, next_pos):
        dir_to = {'U': 1j, 'R': -1, 'D': -1j, 'L': 1}
        trans_id = [-1j, 1, 1j, -1].index(curr_dir)
        if next_pos not in curr_face.jungle_map:
            fs, nf, ts = curr_face.transitions[trans_id]
            next_face = cube_faces[nf]
            next_dir = dir_to[ts]
            next_pos = transitions_map[(fs, ts)](curr_face, next_face, curr_pos)
            return next_face, next_dir, next_pos
        return curr_face, curr_dir, next_pos

    def get_password(final_x, final_y, dir_index):
        return 1000*final_y+4*final_x+dir_index

    return get_password(*walk(transition_fn_2D)), get_password(*walk(transition_fn_3D))