#!/usr/bin/env python3

from get_input import get_input

def has_double(line):
    return any(a == b for a, b in zip(line[1:], line))

def test_has_double():
    assert has_double("aa")
    assert not has_double("a")
    assert not has_double("ab")
    assert has_double("abba")
    assert not has_double("abca")

def vowles(line):
    return sum(1 if c in "aeiou" else 0 for c in line)

def test_vowles():
    assert 0 == vowles('hrwts')
    assert 2 == vowles('arwas')
    assert 2 == vowles('arwas')

def no_substr(line, substrs):
    return not any(substr in line for substr in substrs)

def part1(lines):
    substrs = 'ab, cd, pq, xy'.split(', ')
    return sum(1 for line in lines if
            has_double(line) and 
            vowles(line) >= 3 and 
            no_substr(line, substrs))

def is_sandwich(line):
    return any(a == c != b for a,b,c in zip(line[2:], line[1:], line))

def test_sandwitch():
    assert is_sandwich('aba')
    assert not is_sandwich('aaa')
    assert not is_sandwich('roger')
    assert is_sandwich('dksrsdrdsdfodd')

def two_doubles(word):
    return any(word[i:i+2] in word[i+2:] for i in range(len(word)))

def test_two_doubles():
    assert two_doubles("abab")
    assert not two_doubles('aaa')

def part2(lines):
    return sum(1 for line in lines if
            two_doubles(line) and is_sandwich(line))

if __name__ == '__main__':
    lines = get_input(day=5, year=2015).split('\n')
    print("Part 1: {}".format(part1(lines)))
    print("Part 2: {}".format(part2(lines)))
