#!/usr/bin/env python3

from get_input import get_input
from collections import defaultdict
from itertools import count

def molocule_gen(replacements, init):
    for mol, sub in replacements:
        i = 0
        while True:
            try:
                i += init[i:].index(mol)
            except ValueError:
                break
            yield init[:i] + sub + init[i+len(mol):]
            i += len(mol)

def test_molocule_gen():
    replacements = [
            ('H', 'HO'),
            ('H', 'OH'),
            ('O', 'HH')
            ]
    assert len(set(molocule_gen(replacements, 'HOH'))) == 4

def part1(replacements, init):
    return len(set(molocule_gen(replacements, init)))

def part2(replacements, final):
    replacements = list(reversed(sorted(replacements, key=lambda v: len(v[1]))))
    shortest = None
    seen = set()
    queue = [(0, final, 0)]
    while queue:
        steps, molecule, i = queue.pop()
        if i >= len(replacements) or (shortest and shortest < steps):
            continue
        mol, sub = replacements[i]
        new_molecule = molecule.replace(sub, mol, 1)
        queue.append((steps, molecule, i+1))
        if new_molecule == 'e':
            shortest = steps + 1
            return shortest
        elif new_molecule != molecule and new_molecule not in seen:
            seen.add(new_molecule)
            queue.append((steps+1, new_molecule, 0))
    raise ValueError("Cannot make molecule")

def test_part2():
    replacements = [
            ('H', 'HO'),
            ('H', 'OH'),
            ('O', 'HH'),
            ('e', 'H'),
            ('e', 'O'),
            ]
    assert part2(replacements, 'HOHOHO') == 6

def parse(text):
    lines = text.splitlines()
    replacements = [tuple(line.split(' => '))for line in lines[:-2]]
    return replacements, lines[-1]

if __name__ == '__main__':
    replacements, init = parse(get_input(day=19, year=2015))
    print("Part 1: {}".format(part1(replacements, init)))
    print("Part 2: {}".format(part2(replacements, init)))
