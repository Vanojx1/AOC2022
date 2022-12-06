from functools import reduce

def main(day_input):
    
    def to_prior(l):
        if ord(l) > 96: return ord(l) - 96
        return ord(l) - 38

    def get_prior(group_mapping):
        for g in group_mapping:
            common = reduce(lambda c, n: c & n, g[1:], g[0])
            yield sum([to_prior(l) for l in common])
    
    def get_p1_groups():
        for rucksack in day_input:
            n = len(rucksack)
            yield [set(rucksack[:n//2]), set(rucksack[n//2:])]

    def get_p2_groups():
        for i in range(0, len(day_input), 3):
            yield [set(g) for g in day_input[i:i+3]]

    return sum(get_prior(get_p1_groups())), sum(get_prior(get_p2_groups()))
