#!/usr/bin/env python3

from get_input import get_input
from itertools import product
from copy import deepcopy
import re

#           Cost  Damage  Armor
WEAPONS = """
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0"""

#          Cost  Damage  Armor
ARMOR = """
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
No Armor      0     0       0"""

#           Cost  Damage  Armor
RINGS = """
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
No Ring 1     0     0       0
No Ring 2     0     0       0"""

def fight_gen(boss_stats, player_stats):
    player, boss = deepcopy(player_stats), deepcopy(boss_stats)
    attacker, defender = player, boss
    while True:
        defender['Hit Points'] -= attacker['Damage'] - defender['Armor']
        yield boss, player
        attacker, defender = defender, attacker

def test_fight_gen():
    player = {'Hit Points': 8, 'Damage': 5, 'Armor': 5}
    boss = {'Hit Points': 12, 'Damage': 7, 'Armor': 2}
    for b, p in fight_gen(boss, player):
        print("boss: {}\nplayer: {}".format(b, p))
        print("Boss HP: {}".format(b['Hit Points']))
        print('')
        if b['Hit Points'] <= 0:
            assert p['Hit Points'] == 2
            return

def part1(boss_stats, shop):
    min_cost = None
    for weapon, ring1, ring2, armor in product(
            shop['WEAPONS'].values(),
            shop['RINGS'].values(),
            shop['RINGS'].values(),
            shop['ARMOR'].values()):
        if ring1 == ring2:
            continue
        damage = weapon['damage'] + ring1['damage'] + ring2['damage']
        defence = armor['armor'] + ring1['armor'] + ring2['armor']
        player_stats = {
                'Hit Points': 100,
                'Damage': damage,
                'Armor': defence,
                }
        for b, p in fight_gen(boss_stats, player_stats):
            if p['Hit Points'] <= 0:
                break
            elif b['Hit Points'] <= 0:
                cost = sum(part['cost'] for part in [weapon, ring1, ring2, armor])
                min_cost = min(cost, min_cost) if min_cost != None else cost
                break
    return min_cost

def part2(boss_stats, shop):
    max_cost = None
    for weapon, ring1, ring2, armor in product(
            shop['WEAPONS'].values(),
            shop['RINGS'].values(),
            shop['RINGS'].values(),
            shop['ARMOR'].values()):
        if ring1 == ring2:
            continue
        damage = weapon['damage'] + ring1['damage'] + ring2['damage']
        defence = armor['armor'] + ring1['armor'] + ring2['armor']
        player_stats = {
                'Hit Points': 100,
                'Damage': damage,
                'Armor': defence,
                }
        for b, p in fight_gen(boss_stats, player_stats):
            if p['Hit Points'] <= 0:
                cost = sum(part['cost'] for part in [weapon, ring1, ring2, armor])
                max_cost = max(cost, max_cost) if max_cost != None else cost
                break
            elif b['Hit Points'] <= 0:
                break
    return max_cost
    pass

def parse(text):
    attrs = {}
    shop = {k: {} for k in ['WEAPONS', 'ARMOR', 'RINGS']}
    for thing in shop.keys():
        for line in eval(thing).splitlines():
            if line == '':
                continue
            name, cost, damage, armor = re.split(r' {2,}', line)
            shop[thing][name] = {
                    'name': name,
                    'cost': int(cost),
                    'damage': int(damage),
                    'armor': int(armor),
                    }
    for line in text.splitlines():
        attr, stat = line.split(': ')
        attrs[attr] = int(stat)
    return attrs, shop

if __name__ == '__main__':
    stats, shop = parse(get_input(day=21, year=2015))
    print('Part 1: {}'.format(part1(stats, shop)))
    print('Part 2: {}'.format(part2(stats, shop)))
