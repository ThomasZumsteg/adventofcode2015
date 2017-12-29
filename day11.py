#!/usr/bin/env python3

def password_gen(seed, chars='abcdefghijklnompqrstuvwxyz'):
    password = list(chars.index(s) for s in seed)
    passwd_len = len(password)
    chars_len = len(chars)
    while True:
        for i in reversed(range(passwd_len)):
            password[i] += 1
            if password[i] < chars_len:
                break
            password[i] = 0
        yield ''.join(chars[p] for p in password)

def test_password_gen():
    gen = password_gen('a')
    assert 'b' == next(gen)
    assert 'c' == next(gen)
    gen = password_gen('az')
    assert 'ba' == next(gen)
    gen = password_gen('rs', chars='abcdefghijklnompqrsuvwxyz')
    assert 'ru' == next(gen)
    gen = password_gen('aaabzzz', chars='abdefghijklnompqrstuvwxyz')
    assert 'aaadaaa' == next(gen)

def sequences_of_len_n(string, n):
    m = 0
    i = n
    while i <= len(string):
        if len(set(string[i-n:i])) == 1:
            m += 1
            i += n - 1
        i += 1
    return m

def test_sequences_of_len_n():
    assert 1 == sequences_of_len_n('nii', 2)
    assert 0 == sequences_of_len_n('nii', 3)
    assert 0 == sequences_of_len_n('nue', 2)
    assert 4 == sequences_of_len_n('ekki-ekki-ekki-pitang-zoom-boing', 2)
    assert 0 == sequences_of_len_n('ekki-ekki-ekki-pitang-zoom-boing', 3)

def largest_incr_len(string):
    max_len = 0
    l = 1
    for a, b in zip(string, string[1:]):
        if ord(a) + 1 != ord(b):
            max_len = max(l, max_len)
            l = 0
        l += 1
    return max(max_len, l)

def test_largest_incr_len():
    assert largest_incr_len('abcde') == 5
    assert largest_incr_len('aabcdeee') == 5
    assert largest_incr_len('aabxdeee') == 2

def part1(start):
    for password in password_gen(start, chars='abcdefghjknmpqrstuvwxyz'):
        if sequences_of_len_n(password, 2) == 2 and largest_incr_len(password) >= 3:
            return password

def part2(start):
    nth = 0
    for password in password_gen(start, chars='abcdefghjknmpqrstuvwxyz'):
        if sequences_of_len_n(password, 2) == 2 and largest_incr_len(password) >= 3:
            nth += 1
            if nth == 2:
                return password

if __name__ == '__main__':
    inp = 'cqjxjnds'
    print("Part 1: {}".format(part1(inp)))
    print("Part 2: {}".format(part2(inp)))

