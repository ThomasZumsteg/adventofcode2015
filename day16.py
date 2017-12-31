#!/usr/bin/env python3

from get_input import get_input, line_parser
import operator


def filter_aunts(aunts, props):
    for prop, test in props.items():
        new_aunts = {}
        for a, props in aunts.items():
            if prop not in props or test(props[prop]):
                new_aunts[a] = props
        aunts = new_aunts
    return aunts

def part1(aunts, known_pros=None):
    props = {
        'children': lambda v: v == 3,
        'cats': lambda v: v == 7,
        'samoyeds': lambda v: v == 2,
        'pomeranians': lambda v: v == 3,
        'akitas': lambda v: v == 0,
        'vizslas': lambda v: v == 0,
        'goldfish': lambda v: v == 5,
        'trees': lambda v: v == 3,
        'cars': lambda v: v == 2,
        'perfumes': lambda v: v == 1,
    }
    aunts = filter_aunts(aunts, props)
    assert len(aunts) == 1
    return list(aunts.keys())[0]

def part2(aunts, known_pros=None, compare=None):
    props = {
        'children': lambda v: v == 3,
        'cats': lambda v: v > 7,
        'samoyeds': lambda v: v == 2,
        'pomeranians': lambda v: v < 3,
        'akitas': lambda v: v == 0,
        'vizslas': lambda v: v == 0,
        'goldfish': lambda v: v < 5,
        'trees': lambda v: v > 3,
        'cars': lambda v: v == 2,
        'perfumes': lambda v: v == 1,
    }
    aunts = filter_aunts(aunts, props)
    assert len(aunts) == 1
    return list(aunts.keys())[0]

def parse(line):
    aunt_n = line.index(':')
    aunt = int(line[4:aunt_n])
    props = {}
    for prop in line[aunt_n+2:].split(', '):
        k, v = prop.split(': ') 
        props[k] = int(v)
    return (aunt, props)

if __name__ == '__main__':
    aunts = dict(line_parser(get_input(day=16, year=2015), parse=parse))
    # Part 1: 103
    # Part 2: 405
    print("Part 1: {}".format(part1(aunts)))
    print("Part 2: {}".format(part2(aunts)))
