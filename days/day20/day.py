from collections import deque
from functools import reduce

def main(day_input):
    file = list(map(int, day_input))

    flen = len(file)

    def mix(pairs):
        for original_index in range(flen):
            while pairs[0][0] != original_index: pairs.rotate(-1) 
            current_pair = pairs.popleft() 
            shift = current_pair[1] % (flen-1)
            pairs.rotate(-shift)
            pairs.append(current_pair)
        return pairs

    def get_groove(pairs):
        mixed = [val[1] for val in pairs]
        i0 = mixed.index(0)
        return mixed[(1000+i0)%flen], mixed[(2000+i0)%flen], mixed[(3000+i0)%flen]
    
    actual_file = [n*811589153 for n in file]

    return sum([*get_groove(mix(deque(list(enumerate(file.copy())))))]), \
           sum([*get_groove(reduce(lambda c, _: mix(c), range(10), deque(list(enumerate(actual_file.copy())))))])

