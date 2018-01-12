#!/usr/bin/env python3

from get_input import get_input, line_parser
from itertools import combinations 

def split_gen(items, compartments):
    items.sort(key=lambda x: -x)
    goal = sum(items) / compartments
    for n in range(1, len(items) - 2):
        for combo in combinations(items, n):
            if sum(combo) == goal:
                yield combo

def part1(weights):
    quantum, items = None, None
    for group_a in split_gen(weights, 3):
        if items and len(group_a) > items:
            return quantum
        items = len(group_a)
        quantum = min(quantum or product(group_a), product(group_a))

def product(items):
    total = 1
    for n in items:
        total *= n
    return total

def part2(weights):
    quantum, items = None, None
    for group_a in split_gen(weights, 4):
        if items and len(group_a) > items:
            return quantum
        items = len(group_a)
        quantum = min(quantum or product(group_a), product(group_a))

if __name__ == '__main__':
    weights = line_parser(get_input(day=24, year=2015))
    print("Part 1: {}".format(part1(weights)))
    print("Part 2: {}".format(part2(weights)))
