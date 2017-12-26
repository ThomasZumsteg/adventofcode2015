#!/usr/bin/env python3

from get_input import get_input
import re
from itertools import product

instructions = re.compile(
        r'(toggle|turn off|turn on) (\d+),(\d+) through (\d+),(\d+)')

def apply(grid, func, range_a, range_b):
    for m, n in product(range_a, range_b):
        grid[m][n] = func(grid[m][n])
    return grid

def test_apply():
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    grid = apply(grid, 'turn on', range(0,1000), range(0,1))
    assert sum(sum(row) for row in grid) == 1000

def part1(lines):
    def modes(mode):
        if mode == 'turn on':
            return lambda _: 1
        elif mode == 'turn off':
            return lambda _: 0
        elif mode == 'toggle':
            return lambda v: 0 if v == 1 else 1
        else:
            raise ValueError("Not a valid instruction {}".format(mode))

    grid = [[0 for _ in range(1000)] for _ in range(1000)]

    for line in lines:
        m = instructions.match(line)
        if m is None:
            raise ValueError("Not a valid line {}".format(line))
        mode, args = m.group(1), [int(arg) for arg in m.groups()[1:]]
        grid = apply(grid, modes(mode), range(args[0], args[2]+1), 
                range(args[1], args[3]+1))
    return sum(sum(row) for row in grid)

def part2(lines):
    def modes(mode):
        if mode == 'turn on':
            return lambda v: v + 1
        elif mode == 'turn off':
            return lambda v: v - 1 if v > 0 else 0
        elif mode == 'toggle':
            return lambda v: v + 2
        else:
            raise ValueError("Not a valid instruction {}".format(mode))

    grid = [[0 for _ in range(1000)] for _ in range(1000)]

    for line in lines:
        m = instructions.match(line)
        if m is None:
            raise ValueError("Not a valid line {}".format(line))
        mode, args = m.group(1), [int(arg) for arg in m.groups()[1:]]
        grid = apply(grid, modes(mode), range(args[0], args[2]+1), 
                range(args[1], args[3]+1))
    return sum(sum(row) for row in grid)

if __name__ == '__main__':
    lines = get_input(day=6, year=2015).splitlines()
    print("Part 1: {}".format(part1(lines)))
    print("Part 2: {}".format(part2(lines)))
