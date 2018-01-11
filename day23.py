#!/usr/bin/env python3

from get_input import get_input, line_parser
import re
from copy import deepcopy
from functools import wraps

def part1(computer):
    computer = deepcopy(computer)
    for c in computer:
        pass
        # print('{:3}: {}: {}'.format(c.i, c.ins.__name__, c.registers))
    return c.registers['b']

def part2(computer):
    computer = deepcopy(computer)
    computer.registers['a'] = 1
    for c in computer:
        pass
        # print('{:3}: {}: {}'.format(c.i, c.ins.__name__, c.registers))
    return c.registers['b']

INSTRUCTIONS = {}
class Computer(object):

    def __init__(self, program, i=0, registers=None):
        if registers is None:
            registers = {'a': 0, 'b': 0}
        self.program = program
        self.registers = registers
        self.i = i

    def __iter__(self):
        while 0 <= self.i < len(self.program):
            yield self
            self.program[self.i](self)

    @property
    def ins(self):
        return self.program[self.i]

    def instruction(func):
        @wraps(func)
        def wrapper(self, r, *args):
            initial = self.i
            args = (a if a not in self.registers else se.registers[a] for a in args)
            if r in self.registers:
                rval = func(self, self.registers[r], *args)
                if rval is not None:
                    self.registers[r] = rval
            else:
                func(self, r, *args)
            if self.i == initial:
                self.i += 1
        INSTRUCTIONS[func.__name__] = wrapper
        return wrapper

    @staticmethod
    def partial(func, *partial_args):
        f = INSTRUCTIONS[func]
        @wraps(f)
        def part(self):
            return f(self, *partial_args)
        return part

    @instruction
    def hlf(self, val):
        return val//2

    @instruction
    def tpl(self, val):
        return val * 3

    @instruction
    def inc(self, val):
        return val + 1

    @instruction
    def jmp(self, offset):
        self.i += offset

    @instruction
    def jie(self, r, offset):
        if r % 2 == 0:
            self.i += offset

    @instruction
    def jio(self, r, offset):
        if r == 1:
            self.i += offset

    @staticmethod
    def parse(lines):
        c = Computer([])
        for line in lines.splitlines():
            program_name, *args = re.split(r',? ', line)
            vals = []
            for a in args:
                try:
                    vals.append(int(a))
                except ValueError:
                    vals.append(a)
            ins = Computer.partial(program_name, *vals)
            c.program.append(ins)
        return c

if __name__ == '__main__':
    computer = Computer.parse(get_input(day=23, year=2015))
    print("Part 1: {}".format(part1(computer)))
    print("Part 2: {}".format(part2(computer)))
