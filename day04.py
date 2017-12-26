#!/usr/bin/env python3

from hashlib import md5
from itertools import count

def part1(inp):
    for i in count(1):
        digest = md5('{}{}'.format(inp, i).encode('ascii')).hexdigest()
        if digest[:5] == '0' * 5:
            return i

def part2(inp):
    for i in count(1):
        digest = md5('{}{}'.format(inp, i).encode('ascii')).hexdigest()
        if digest[:6] == '0' * 6:
            return i

if __name__ == '__main__':
    inp = 'yzbqklnj'
    print("Part 1: {}".format(part1(inp)))
    print("Part 2: {}".format(part2(inp)))
