#!/usr/bin/env python3

from get_input import get_input

def elevator(items, up, down):
    floor = 0
    for item in items:
        if item == up:
            floor += 1
        elif item == down:
            floor -= 1
        yield floor

def part1(line):
    for floor in elevator(line, '(', ')'):
        pass
    return floor

def part2(line):
    for i, floor in enumerate(elevator(line, '(', ')'), 1):
        if floor < 0:
            return i

if __name__ == '__main__':
    lines = get_input(day=1, year=2015)
    # Part 1: 232
    # Part 2: 1782
    print("Part 1: {}".format(part1(lines)))
    print("Part 2: {}".format(part2(lines)))
