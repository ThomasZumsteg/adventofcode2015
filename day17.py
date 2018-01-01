#!/usr/bin/env python3

from get_input import get_input, line_parser

def storage_gen(buckets, volume):
    queue = [(0, [])]
    while queue:
        i, used = queue.pop()
        if sum(used) == volume:
            yield tuple(used)
        elif sum(used) < volume and i < len(buckets):
            queue.append((i+1, used + [buckets[i]]))
            queue.append((i+1, used))

def test_storage_gen():
    buckets = [15, 10, 5, 5, 20]
    assert len(list(storage_gen(buckets, 25))) == 4

def part1(buckets, volume=150):
    count = 0
    for b in storage_gen(buckets, volume):
        count += 1
    return count

def part2(buckets, volume=150):
    shortest = []
    for b in storage_gen(buckets, volume):
        if shortest == [] or len(b) < len(shortest[0]):
            shortest = [b]
        elif len(b) == len(shortest[0]):
            shortest.append(b)
    return len(shortest)

if __name__ == '__main__':
    buckets = line_parser(get_input(day=17, year=2015))
    print("Part 1: {}".format(part1(buckets)))
    print("Part 2: {}".format(part2(buckets)))
