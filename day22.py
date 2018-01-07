#!/usr/bin/env python3

from get_input import get_input
from copy import copy

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
        def wrapped(caster):
            print('Casting {}'.format(spell.__name__))
            if cost > caster['mana']:
                raise SpellException('Out of mana')
            if caster.get(spell.__name__, 0) > 0:
                raise SpellException('{} Cooldown {}'.format(spell.__name__,
                    caster[spell.__name__]))
            caster[spell.__name__] = cooldown
            caster['mana'] -= cost + 0 if caster['Recharge'] <= 0 else 110
            caster['mana used'] += cost
            attack_val = spell(caster)
            return attack_val + 0 if caster['Poison'] <= 0 else 3
        return wrapped
    SPELLS.append(cast_spell)
    return cast_spell

@spell(53)
def magic_missle(caster):
    return 4

@spell(73)
def drain(caster):
    caster['Hip Points'] += 2
    return 2

@spell(113, cooldown=6)
def Shield(caster):
    return 0

@spell(173, cooldown=6)
def Poison(caster):
    return 0

@spell(229, cooldown=5)
def Recharge(caster):
    return 0

def part1(player, boss):
    min_mana = None
    queue = [(player, boss)]
    while queue:
        player, boss = queue.pop()
        for spell in SPELLS:
            clone_p, clone_b = copy(player), copy(boss)
            print(spell)
            try:
                clone_b['Hit Points'] -= spell(clone_p)
            except SpellException as e:
                print("Oops {}".format(e))
                continue
            if clone_b.hp <= 0:
                min_mana = min(min_mana or clone_p['mana used'], clone_p['mana used'])
            defence = 7 if clone_p.get('Shield',0) > 0 else 0
            clone_p.hp -= max(1, clone_b['Damage'] - defence)
            if clone_p.hp > 0:
                queue.append((clone_p, clone_b))
    return min_mana

def part2(player, boss):
    pass

def parse(text):
    boss = {'Hit Points': None, 'Attack': None}
    for line in text.splitlines():
        vals = line.split(': ')
        if vals[0] in boss:
            boss[vals[0]] = int(vals[1])
    return boss, {'mana': 500, 'Hit Points': 50}

if __name__ == '__main__':
    boss, player = parse(get_input(day=22, year=2015))
    print("Part 1: {}".format(part1(player, boss)))
    print("Part 2: {}".format(part2(player, boss)))
