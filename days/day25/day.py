import re

def main(day_input):
    snafu_int = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
    int_snafu = {v:k for k,v in snafu_int.items()}

    max_l = max(map(len, day_input))
    snafu_sum = ''

    carry = 0
    for col in range(max_l):
        sum_col = carry + sum([snafu_int[snafu[::-1][col]] for snafu in day_input if col < len(snafu)])
        carry = 0
        while sum_col > 2:
            carry += 1
            sum_col -= 5
            
        while sum_col < -2:
            carry -= 1
            sum_col += 5
        
        snafu_sum += int_snafu[sum_col]

    snafu_sum = snafu_sum[::-1]

    return snafu_sum, None