#!/usr/bin/env python3

from get_input import get_input
from collections import defaultdict
from functools import wraps
from copy import deepcopy

SPELLS = []

class SpellException(Exception):
    pass

# Magic Missile costs 53 mana. It instantly does 4 damage.
# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
# Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
# Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
def spell(cost, cooldown=0):
    def cast_spell(spell):
        @wraps(spell)
        def wrapped(caster):
            if cost > caster['mana']:
                raise SpellException('Out of mana')
            if caster[spell.__name__] > 0:
                raise SpellException('{} Cooldown {}'.format(spell.__name__,
                    caster[spell.__name__]))
            caster[spell.__name__] = cooldown + 1
            caster['mana'] -= cost
            caster['mana used'] += cost
            caster['spells'].append(spell.__name__)
            tick(caster)
            return spell(caster)
        SPELLS.append(wrapped)
        return wrapped
    return cast_spell

def tick(caster):
    for s in SPELLS:
        caster[s.__name__] -= 1

@spell(53)
def magic_missle(caster):
    return 4

@spell(73)
def drain(caster):
    caster['Hit Points'] += 2
    return 2

@spell(113, cooldown=6)
def shield(caster):
    return 0

@spell(173, cooldown=6)
def poison(caster):
    return 0

@spell(229, cooldown=5)
def recharge(caster):
    return 0

def worth_it(player, boss, min_mana):
    if min_mana is None:
        return True
    if player['Hit Points'] <= 0 or boss['Hit Points'] <= 0:
        return False
    if boss['player']:
        player, boss = boss, player
    return player['mana used'] < min_mana

def part1(player, boss):
    min_mana = None
    queue = [(player, boss)]
    while queue:
        attacker, defender = queue.pop()
        for attack in attacker['attacks']:
            a, d = deepcopy(attacker), deepcopy(defender)
            defender_is_player = d['player']

            defence = 0
            if defender_is_player:
                defence = 7 if d['shield'] > 0 else 0
                d['mana'] += 0 if d['recharge'] <= 0 else 101
                a['Hit Points'] -= 0 if d['poison'] <= 0 else 3
                tick(d)
            else:
                a['mana'] += 0 if a['recharge'] <= 0 else 101
                d['Hit Points'] -= 0 if a['poison'] <= 0 else 3

            try:
                d['Hit Points'] -= max(1 if defender_is_player else 0,
                        attack(a) - defence)
            except SpellException as e:
                continue

            if d['Hit Points'] <= 0 and not defender_is_player:
                min_mana = min(min_mana or a['mana used'], a['mana used'])
            if d['Hit Points'] > 0 and worth_it(a, d, min_mana):
                x, y = a, d
                if defender_is_player:
                    y, x = x, y
                # print('{} {:4} Boss: {:2} Player: {:2} {:3} {}'.format(
                #     'B' if defender_is_player else 'P', min_mana, y['Hit Points'],
                #     x['Hit Points'], x['mana'],','.join(x['spells'])))
                queue.append((d, a))
    return min_mana

def test_part1():
    player = defaultdict(int, 
            {'mana': 500, 'Hit Points': 50, 'mana used': 0, 'spells': []})
    boss = {"Hit Points": 13, 'Damage': 8}
    assert 3 == poison(player)

def part2(player, boss):
    min_mana = None
    queue = [(player, boss)]
    while queue:
        attacker, defender = queue.pop()
        for attack in attacker['attacks']:
            a, d = deepcopy(attacker), deepcopy(defender)
            defender_is_player = d['player']

            defence = 0
            if defender_is_player:
                defence = 7 if d['shield'] > 0 else 0
                d['mana'] += 0 if d['recharge'] <= 0 else 101
                a['Hit Points'] -= 0 if d['poison'] <= 0 else 3
                tick(d)
            else:
                a['Hit Points'] -= 1
                a['mana'] += 0 if a['recharge'] <= 0 else 101
                d['Hit Points'] -= 0 if a['poison'] <= 0 else 3

            try:
                d['Hit Points'] -= max(1 if defender_is_player else 0,
                        attack(a) - defence)
            except SpellException as e:
                continue

            if (d['Hit Points'] <= 0 and not defender_is_player) or \
                (a['Hit Points'] <= 0 and defender_is_player):
                if defender_is_player:
                    a = d
                min_mana = min(min_mana or a['mana used'], a['mana used'])
            if worth_it(a, d, min_mana):
                x, y = a, d
                if defender_is_player:
                    y, x = x, y
                print('{} {:4} Boss: {:2} Player: {:2} {:3} {}'.format(
                    'B' if defender_is_player else 'P', min_mana, y['Hit Points'],
                    x['Hit Points'], x['mana'],','.join(x['spells'])))
                queue.append((d, a))
    return min_mana

def parse(text):
    boss = {'Hit Points': None, 'Damage': None}
    for line in text.splitlines():
        if line == '':
            continue
        k, v = line.split(': ')
        boss[k] = int(v)
    boss['attacks'] = [lambda _: boss['Damage']]
    boss['player'] = False
    player = {'mana': 500, 'Hit Points': 50, 'mana used': 0, 'spells': [],
            'attacks': SPELLS, 'player': True}
    return boss, defaultdict(int, player)

if __name__ == '__main__':
    boss, player = parse(get_input(day=22, year=2015))
    # print("Part 1: {}".format(part1(player, boss)))
    print("Part 2: {}".format(part2(player, boss)))
