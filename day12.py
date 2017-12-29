#!/usr/bin/env python3

from get_input import get_input
from json import loads

def find_numbers(doc, ignore=None):
    ignore = ignore or []
    queue = [doc]
    total = 0
    while queue:
        item = queue.pop()
        if type(item) is int:
            total += item
        elif type(item) is dict:
            item_values = item.values()
            if not any(ignored in item_values for ignored in ignore):
                queue.extend(item_values)
        elif type(item) is list:
            queue.extend(item)
    return total

def part1(doc):
    return find_numbers(doc)

def part2(doc):
    return find_numbers(doc, ignore=['red'])

if __name__ == '__main__':
    json_doc = loads(get_input(day=12, year=2015))
    print("Part 1: {}".format(part1(json_doc)))
    print("Part 2: {}".format(part2(json_doc)))
