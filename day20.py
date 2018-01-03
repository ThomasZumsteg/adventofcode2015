#!/usr/bin/env python3

from itertools import count

def part1(limit):
    n_houses = ((limit+1) // 10)
    houses = [10] * n_houses
    for elf in range(2, n_houses):
        for n in range(elf, n_houses, elf):
            houses[n] += 10 * elf
    for house, presents in enumerate(houses[1:], 1):
        if presents > limit:
            return house 

def part2(limit):
    biggest = 0 
    for house in count(1):
        total = 0
        for nth in range(1, 51):
            if house % nth == 0:
                total += (house // nth) * 11
        if total > limit:
            return house

if __name__ == '__main__':
    inp = 36000000
    # Part 1: 831600
    # Part 2: 884520
    print("Part 1: {}".format(part1(inp)))
    print("Part 2: {}".format(part2(inp)))
