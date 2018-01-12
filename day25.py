#!/usr/bin/env python3

from get_input import get_input
import re

def start_mult_mod(start, mult, mod):
    num = start
    while True:
        yield num
        num = (num * mult) % mod

def part1(row, col, gen=None):
    if gen is None:
        gen = start_mult_mod(20151125, 252533, 33554393)
    nth = ((row + col - 2) * (row + col - 1)) // 2 + col
    return (nth * 20151125 * 252533) % 33554393
    for n, num in enumerate(gen, 1):
        if n == nth:
            return num

def part2(row, col):
    return "Happy Holidays!"

def parse(text):
    m = re.search(r"Enter the code at row (\d+), column (\d+)", text)
    return (int(g) for g in m.groups())

if __name__ == '__main__':
    row, col = parse(get_input(day=25, year=2015))
    print("Part 1: {}".format(part1(row, col)))
    print("Part 2: {}".format(part2(row, col)))
