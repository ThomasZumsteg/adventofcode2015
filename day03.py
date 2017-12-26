#!/usr/bin/env python3

from get_input import get_input, line_parser

def directions_gen(directions):
    pos = (0, 0)
    dirs = {'<': (0, -1), '>': (0, 1), '^': (1, 0), 'v': (-1, 0)}
    for char in directions:
        if char in dirs:
            pos = tuple(p + d for p, d in zip(pos, dirs[char]))
        yield pos

def part1(line):
    return len(set(p for p in directions_gen(line)))

def part2(line):
    santa = set(p for p in directions_gen(
        [d for i, d in enumerate(line) if i % 2 == 0]))
    robot_santa = set(p for p in directions_gen(
        [d for i, d in enumerate(line) if i % 2 == 1]))
    return len(robot_santa.union(santa))
    

def parse(line):
    return line

if __name__ == '__main__':
    line = get_input(day=3, year=2015)
    print("Part 1: {}".format(part1(line)))
    print("Part 2: {}".format(part2(line)))
