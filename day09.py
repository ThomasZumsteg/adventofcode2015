#!/usr/bin/env python3

from get_input import get_input
from collections import defaultdict

def all_paths(locations):
    paths = [[loc] for loc in locations.keys()]
    while True:
        update = []
        for path in paths:
            for dest in locations[path[-1]]:
                if dest not in path:
                    update.append(path + [dest])
        if update == []:
            return paths
        paths = update

def part1(locations):
    paths = all_paths(locations)
    return min(sum(locations[a][b] for a, b in zip(path, path[1:])) for path in paths)

def part2(locations):
    paths = all_paths(locations)
    return max(sum(locations[a][b] for a, b in zip(path, path[1:])) for path in paths)

def parse(text):
    locations = defaultdict(dict)
    for line in text.splitlines():
        a, _, b, _, dist = line.split()
        locations[a][b] = int(dist)
        locations[b][a] = int(dist)
    return locations

if __name__ == '__main__':
    locations = parse(get_input(day=9, year=2015))
    print("Part 1: {}".format(part1(locations)))
    print("Part 2: {}".format(part2(locations)))
