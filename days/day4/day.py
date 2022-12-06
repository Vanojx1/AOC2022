def main(day_input):
    full_overlap = 0
    overlap = 0
    for elf1, elf2 in map(lambda p: p.split(','), day_input):
        s1, e1 = map(int, elf1.split('-'))
        s2, e2 = map(int, elf2.split('-'))

        (s1, e1), (s2, e2) = sorted([(s1, e1), (s2, e2)])

        if s1 <= s2 and e1 >= s2 or s1 >= s2 and e1 >= e2:
            overlap += 1
            if s1 >= s2 and e1 <= e2 or s2 >= s1 and e2 <= e1:
                full_overlap += 1

    return full_overlap, overlap