#!/usr/bin/env python3

from get_input import get_input, line_parser
import re

def part1(ingredients, limit=100):
    max_score = 0
    for dist in distribute_gen(len(ingredients), limit):
        score = 1
        for attr in ['capacity', 'durability', 'flavor', 'texture']:
            attr_score = 0
            for i, d in zip(ingredients, dist):
                attr_score += i[attr] * d
            score *= attr_score if attr_score > 0 else 0
        max_score = max(max_score, score)
    return max_score

test_text = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

def test_part1():
    ingredients = line_parser(test_text, parse=parse)
    assert 62842880 == part1(ingredients)

def part2(ingredients, limit=100, calories=500):
    max_score = 0
    for dist in distribute_gen(len(ingredients), limit):
        if sum(i['calories'] * d for i, d in zip(ingredients, dist)) != calories:
            continue
        score = 1
        for attr in ['capacity', 'durability', 'flavor', 'texture']:
            attr_score = 0
            for i, d in zip(ingredients, dist):
                attr_score += i[attr] * d
            score *= attr_score if attr_score > 0 else 0
        max_score = max(max_score, score)
    return max_score

def distribute_gen(buckets, volume):
    dist = [0] * buckets
    dist[0] = volume
    while True:
        yield dist
        dist[0] -= 1
        dist[1] += 1
        if dist[0] < 0:
            i = 1
            while dist[0] < 0:
                if i+1 >= len(dist):
                    raise StopIteration 
                dist[i+1] += 1
                dist[0] += dist[i] - 1
                dist[i] = 0
                i += 1

def parse(line):
    ingredient = re.compile(r'(?P<name>\w+): capacity (?P<capacity>-?\d+), ' +
            'durability (?P<durability>-?\d+), flavor (?P<flavor>-?\d+), ' +
            'texture (?P<texture>-?\d+), calories (?P<calories>-?\d+)')
    m = ingredient.match(line)
    return {k: int(v) if k != 'name' else v for k, v in m.groupdict().items()}

if __name__ == '__main__':
    ingredients = line_parser(get_input(day=15, year=2015), parse=parse)
    print("Part 1: {}".format(part1(ingredients)))
    print("Part 2: {}".format(part2(ingredients)))
