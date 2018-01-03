#!/usr/bin/env python3

from itertools import count

def part1(limit):
    biggest = 0 
    for house in count(1):
        total = 0
        for elf in range(1, int(house**0.5)):
            if elf * elf == house:
                total += 10 * elf
            elif house % elf == 0:
                total += 10 * elf
                total += 10 * house // elf
        if total > limit:
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
    print("Part 1: {}".format(part1(inp)))
    print("Part 2: {}".format(part2(inp)))
