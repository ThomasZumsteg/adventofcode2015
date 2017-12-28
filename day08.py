#!/usr/bin/env python3

from get_input import get_input

def escape(line):
    result = ['"']
    escape_me = r"\"'\\"
    for char in line:
        if char in escape_me:
            result.append('\\')
        result.append(char)
    return ''.join(result) + '"'

def test_escape():
    assert escape('""') == r'"\"\""'
    assert escape('"abc"') == r'"\"abc\""'
    assert escape(r'"aaa\"aaa"') == r'"\"aaa\\\"aaa\""'
    assert escape(r'"\x27"') == r'"\"\\x27\""'
    for line in get_input(day=8, year=2015).splitlines():
        assert line == code(escape(line))

def code(line):
    if not (line[0] == line[-1] == '"'):
        raise ValueError('Not a valid string {}'.format(line))
    i = 1
    result = []
    while i < len(line) - 1:
        if line[i:i+2] == '\\x':
            result.append(chr(int(line[i+2:i+4], 16)))
            i += 3
        elif line[i:i+1] == '\\':
            result.append(line[i+1])
            i += 1
        else:
            result.append(line[i])
        i += 1
    return ''.join(result)

def test_code():
    assert code('""') == ''
    assert code('"abc"') == 'abc'
    assert code('"aaa\"aaa"') == 'aaa"aaa'
    assert code('"\x27"') == "'"
    for line in get_input(day=8, year=2015).splitlines():
        assert eval(line) == code(line)

def part1(lines):
    return sum(len(line) - len(code(line)) for line in lines)

def part2(lines):
    return sum(len(escape(line)) - len(line) for line in lines)

if __name__ == '__main__':
    lines = get_input(day=8, year=2015).splitlines()
    print("Part 1: {}".format(part1(lines)))
    print("Part 2: {}".format(part2(lines)))
