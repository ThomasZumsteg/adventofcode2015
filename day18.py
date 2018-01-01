#!/usr/bin/env python3

from get_input import get_input
from itertools import product

def game_of_lights(start, stuck=None):
    rows, cols = len(start), len(start[0])
    lights = start
    while True:
        new_lights = [[None for _ in range(cols)] for _ in range(rows)]
        for r, c in product(range(rows), range(cols)):
            new_lights[r][c] = lights[r][c]
            if stuck is not None and (r, c) in stuck:
                continue
            neighbors_on = 0
            for n, m in product(range(r-1, r+2), range(c-1, c+2)):
                if 0 <= n < rows and 0 <= m < cols and not (n == r and m == c) and \
                    '#' == lights[n][m]:
                    neighbors_on += 1
            if lights[r][c] == '#' and neighbors_on not in (2, 3):
                    new_lights[r][c] = '.'
            elif lights[r][c] == '.' and 3 == neighbors_on:
                    new_lights[r][c] = '#'
        lights = new_lights
        yield lights

def part1(start, rounds=100):
    for i, lights in enumerate(game_of_lights(start), 1):
        if i == rounds:
            return sum(1 if l == '#' else 0 for row in lights for l in row)

test_text = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

def test_part1():
    test = list(list(l) for l in test_text.splitlines())
    assert part1(test, rounds = 4) == 4

def part2(start, rounds=100):
    start[0][0] = start[-1][0] = start[-1][-1] = start[0][-1] = '#'
    length, width = len(start)-1, len(start[0])-1
    corners = ((0,0), (0, width), (length, 0), (length, width))
    for i, lights in enumerate(game_of_lights(start, stuck=corners), 1):
        if i == rounds:
            return sum(1 if l == '#' else 0 for row in lights for l in row)

def test_part2():
    test = list(list(l) for l in test_text.splitlines())
    assert part2(test, rounds=5) == 17

if __name__ == '__main__':
    # Part 1: 821
    # Part 2: None
    lines = list(list(l) for l in get_input(day=18, year=2015).splitlines())
    print("Part 1: {}".format(part1(lines)))
    print("Part 2: {}".format(part2(lines)))
