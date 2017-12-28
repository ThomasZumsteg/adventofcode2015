#!/usr/bin/env python3

from get_input import get_input, line_parser
import operator
import copy

FUNCTIONS = {
    'NOT': lambda v: ~v % 2**16,
    'AND': operator.and_,
    'OR': operator.or_,
    'RSHIFT': lambda v, s: (v >> s) % (2**16),
    'LSHIFT': lambda v, s: (v << s) % (2**16)
}

def evaluate(reg, env):
    if type(reg) is int:
        return reg
    if type(env[reg]) != int:
        if len(env[reg]) == 1:
            env[reg] = evaluate(env[reg][0], env)
        else:
            args = [evaluate(r, env) for r in env[reg][1:]]
            if env[reg][0] in FUNCTIONS:
                env[reg] = FUNCTIONS[env[reg][0]](*args)
    return env[reg]

def part1(lines):
    env = copy.copy(lines)
    return evaluate('a', env)

def part2(lines):
    env = copy.copy(lines)
    a = evaluate('a', env)
    env = copy.copy(lines)
    env['b'] = a
    return evaluate('a', env)

def test_evaluate():
    test = parse(open('.AoC-2015-07.test').read())
    assert evaluate('d', test) == 72
    assert evaluate('i', test) == 65079
    assert evaluate('g', test) == 114
    assert evaluate('h', test) == 65412
    assert evaluate('f', test) == 492
    assert evaluate('e', test) == 507

def parse(text):
    result = {}
    for line in text.splitlines():
        args, reg = line.split(' -> ')
        args = tuple(int(a) if a.isdigit() else a for a in args.split(' '))
        if len(args) == 3:
            args = (args[1], args[0], args[2])
        result[reg] = args
    return result

if __name__ == '__main__':
    lines = parse(get_input(day=7, year=2015))
    print("Part 1: {}".format(part1(lines)))
    print("Part 2: {}".format(part2(lines)))

