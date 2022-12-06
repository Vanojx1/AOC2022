import re

def reg_gen(l):
    w, s = '\\w', '\\'
    return '(' + ''.join([r'(\w)' + ''.join([rf"(?!{w*k}{s}{n+2})" for k in range(l-n-1)]) for n in range(l)]) + ')'

def main(day_input):
    MARKER_LEN = 4
    MESSAGE_LEN = 14
    buffer = day_input[0]
    m = re.search(re.compile(reg_gen(MARKER_LEN)), buffer)
    marker_start = m.start(1) + MARKER_LEN

    m = re.search(re.compile(reg_gen(MESSAGE_LEN)), buffer)
    message_start = m.start(1) + MESSAGE_LEN
    
    return marker_start, message_start
