#!/usr/bin/env python3

from get_input import get_input, line_parser

def paper(l,w,h):
    sides = (l*w, w*h, h*l)
    return 2 * sum(sides) + min(sides)

def part1(lines):
    return sum(paper(*line) for line in lines)

def ribbon(l,w,h):
    s,m,l = sorted((l,w,h))
    return 2 * (s + m) + s * m * l

def part2(lines):
    return sum(ribbon(*line) for line in lines)

def parse(line):
    return tuple(int(n) for n in line.split('x'))

if __name__ == '__main__':
    lines = line_parser(get_input(day=2, year=2015), parse=parse)
    print("Part 1: {}".format(part1(lines)))
    print("Part 2: {}".format(part2(lines)))
