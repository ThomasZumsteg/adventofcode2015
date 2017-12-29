#!/usr/bin/env python3

from get_input import get_input
from collections import defaultdict
from itertools import permutations
import copy
import re

def part1(lookup):
    persons = list(lookup.keys())
    n_persons = len(persons)
    max_score = None
    for ordering in permutations(persons):
        ordering_score = 0
        for i in range(n_persons):
            person = ordering[i]
            left = ordering[(i-1)%n_persons]
            right = ordering[(i+1)%n_persons]
            ordering_score += lookup[person][left] + lookup[person][right]
        max_score = max(max_score or ordering_score, ordering_score)
    return max_score

test_text = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""

def test_part1():
    lookup = parse(test_text)
    assert 330 == part1(lookup)

def part2(lookup):
    lookup = copy.deepcopy(lookup)
    for v in lookup.values():
        v['self'] = 0
    lookup['self'] = dict((p, 0) for p in lookup.keys())
    return part1(lookup)

def parse(text):
    lookup = defaultdict(dict)
    for line in text.splitlines():
        person_a, gain_lose, num, person_b = re.match(
          r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).',
          line).groups()
        lookup[person_a][person_b] = -int(num) if gain_lose == 'lose' else int(num)
    return lookup

if __name__ == '__main__':
    lookup = parse(get_input(day=13, year=2015))
    print("Part 1: {}".format(part1(lookup)))
    print("Part 2: {}".format(part2(lookup)))
