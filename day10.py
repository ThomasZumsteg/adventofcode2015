#!/usr/bin/env python3

def look_and_say(inp):
    groups = [[inp[0]]]
    for c in inp[1:]:
        if c == groups[-1][0]:
            groups[-1].append(c)
        else:
            groups.append([c])
    return ''.join('{}{}'.format(len(g),g[0]) for g in groups)

def test_look_and_say():
    assert look_and_say('1') == '11'
    assert look_and_say('11') == '21'
    assert look_and_say('111') == '31'
    assert look_and_say('1112') == '3112'
    assert look_and_say('21') == '1211'
    assert look_and_say('1211') == '111221'
    assert look_and_say('111221') == '312211'

def part1(inp, times=40):
    for _ in range(times):
        inp = look_and_say(inp)
    return len(inp)

def part2(inp, times=50):
    return part1(inp, times=times)

if __name__ == '__main__':
    inp = '1113122113'
    print("Part 1: {}".format(part1(inp)))
    print("Part 2: {}".format(part2(inp)))
