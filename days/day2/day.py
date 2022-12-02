def main(day_input):
    # A,X Rock
    # B,Y paper
    # C,Z Scissor

    conv = {'A':1,'B':2,'C':3,'X':1,'Y':2,'Z':3}
    lose_from = {1:2,2:3,3:1}
    lose_to = {2:1,3:2,1:3}
    what_to_play = {
        1: lambda x: lose_to[x],
        2: lambda x: x,
        3: lambda x: [1,2,3,1][x]
    }

    def play(part=1):
        for r in day_input:
            OPP, ME = (lambda A, B: (conv[A], conv[B]))(*r.split(' '))
            if part == 2: ME = what_to_play[ME](OPP)
            if ME == OPP: yield ME + 3
            elif lose_from[ME] == OPP: yield ME
            else: yield ME + 6
    
    return sum(play()), sum(play(2))
