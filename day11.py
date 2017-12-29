#!/usr/bin/env python3

def password_gen(seed, avoid=None):
    password = list(seed)
    while True:
        for i, char in reversed(list(enumerate(password))):
            password[i] = chr(ord(char) + 1)
            if char < 'z':
                break
            password[i] = 'a'
        for i, char in enumerate(password):
            if avoid and char in avoid:
                password[i] = char
                password[i+1:] = 'z' * (len(password) - i - 1) 
                break
        else:
            yield ''.join(password)

def test_password_gen():
    gen = password_gen('a')
    assert 'b' == next(gen)
    assert 'c' == next(gen)
    gen = password_gen('az')
    assert 'ba' == next(gen)
    gen = password_gen('rs', avoid = 't')
    assert 'ru' == next(gen)
    gen = password_gen('aaabzzz', avoid = 'c')
    assert 'aaadaaa' == next(gen)

def pair_sequences(phrase):
    i = 1
    sequences = set()
    while i < len(phrase):
        if phrase[i] == phrase[i-1]:
            sequences.add(phrase[i])
            i += 2
        else:
            i += 1
    return sequences

def part1(start):
    for password in password_gen(start, avoid='ilo'):
        print(password)
        if 2 >= len(pair_sequences(password)) and \
            any(ord(a) + 2 == ord(b) + 1 == c for a, b, c 
                in zip(password, password[1:], password[2:])):
            return password

def part2(start):
    pass

if __name__ == '__main__':
    inp = 'cqjxjnds'
    print("Part 1: {}".format(part1(inp)))
    print("Part 2: {}".format(part2(inp)))

