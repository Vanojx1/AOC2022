from utils import Point
import heapq

def main(day_input):
    max_x = len(day_input[0])-1
    max_y = len(day_input)-1
    dir_map = {'^': -1j, '>': 1, 'v': 1j, '<': -1}
    blizzards = [(str(id), *b) for id, b in enumerate([(Point(x, y), dir_map[v]) for y, row in enumerate(day_input) for x, v in enumerate(row) if v in '<>^v'])]
    valley_in = Point(1, 0)
    valley_out = Point(max_x-1, max_y)

    def transition(b, d):
        if d == 1 and b.x == max_x:  return Point(1, b.y)
        if d == -1 and b.x == 0:     return Point(max_x-1, b.y)
        if d == 1j and b.y == max_y: return Point(b.x, 1)
        if d == -1j and b.y == 0:    return Point(b.x, max_y-1)
        return b

    def get_state(b):
        return tuple((id, pos) for id, pos, _ in sorted(b, key=lambda x: x[1]))

    states = set([get_state(blizzards)])    
    states_list = [set([p for id, p, d in blizzards])]
    curr_b = blizzards.copy()
    while True:
        next_b_points = [transition(p+d, d) for id, p, d in curr_b]
        curr_b = [(id, p, d) for p, (id, _, d) in zip(next_b_points, curr_b)]
        new_state = get_state(curr_b)
        if new_state in states: break
        states.add(new_state)
        states_list.append(set(next_b_points))
    states_n = len(states_list)

    def through_the_valley(from_p, to_p, start_state=0):
        q = [(0, from_p.mdist(to_p), [(start_state, from_p)])]
        heapq.heapify(q)
        visited = set([(start_state, from_p)])
        
        while q:

            steps, d, path = heapq.heappop(q)
            state_i, curr_p = path[-1]

            if curr_p == to_p:
                return steps, state_i
            
            next_state_i = (state_i + 1) % states_n

            if (next_state_i, curr_p) not in visited and curr_p not in states_list[next_state_i]:
                heapq.heappush(q, (steps+1, d, path + [(next_state_i, curr_p)]))
                visited.add((next_state_i, curr_p))

            for next_p in [curr_p+o for o in (-1j, 1, 1j, -1)]:
                if next_p == to_p or (
                (next_state_i, next_p) not in visited and \
                0 < next_p.x < max_x and \
                0 < next_p.y < max_y and \
                next_p not in states_list[next_state_i]):
                    visited.add((next_state_i, next_p))
                    heapq.heappush(q, (steps+1, next_p.mdist(to_p), path + [(next_state_i, next_p)]))

    steps1, f_state = through_the_valley(valley_in, valley_out)
    steps2, f_state = through_the_valley(valley_out, valley_in, f_state)
    steps3, _       = through_the_valley(valley_in, valley_out, f_state)

    return steps1, steps1 + steps2 + steps3