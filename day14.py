#!/usr/bin/env python3

from get_input import get_input, line_parser
import re

def part1(reindeer, time=2503):
    return max(r.distance(time) for r in reindeer) 

test_text = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""

def test_part1():
    reindeer = line_parser(test_text, parse=parse)
    assert part1(reindeer, time=1000) == 1120

def part2(reindeer, time=2503):
    scores = dict((r.name, 0) for r in reindeer)
    for s in range(1, time):
        leaders = sorted((r.distance(s), r.name) for r in reindeer)
        leaders.reverse()
        leader = leaders[0][0]
        for d, name in leaders:
            if d != leader:
                break
            scores[name] += 1
    return max(scores.values())

def test_part2():
    reindeer = line_parser(test_text, parse=parse)
    assert part2(reindeer, time=1000) == 689

class Reindeer(object):
    def __init__(self, name, speed, time, rest):
        self.name = name
        self.speed = int(speed)
        self.time = int(time)
        self.rest = int(rest)

    def distance(self, time):
        location = 0
        while True:
            if time <= self.time:
                return location + time * self.speed
            location += self.speed * self.time
            time -= self.time
            if time <= self.rest:
                return location
            time -= self.rest

def parse(line):
    form = re.compile(r'(?P<name>\w+) can fly (?P<speed>\d+) km/s for ' + \
        '(?P<time>\d+) seconds, but then must rest for (?P<rest>\d+) seconds.')
    m = form.match(line)
    return Reindeer(**m.groupdict())

if __name__ == "__main__":
    reindeer = line_parser(get_input(day=14, year=2015), parse=parse)
    print("Part 1: {}".format(part1(reindeer)))
    print("Part 2: {}".format(part2(reindeer)))
