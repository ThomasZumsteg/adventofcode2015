#!/usr/bin/env python3

from get_input import get_input
from collections import defaultdict
from functools import wraps
from copy import deepcopy

class Boss(object):
    def __init__(self, hp, attack, defence=0):
        self.hp = hp
        self.callbacks = []
        self.player = False
        self.defence = 0
        self.attack = attack
        self.attacks = [Boss.simple_attack]

    def simple_attack(attacker, defender):
        attacker.tick()
        defender.tick()
        if attacker.hp > 0:
            defender.hp -= max(1, attacker.attack - defender.defence)

    def tick(caster):
        callbacks, caster.callbacks = caster.callbacks, []
        for call in callbacks:
            call(caster)

    def add_callback(self, callback):
        self.callbacks.append(callback)

class SpellException(Exception):
    pass

SPELLS = []

class Player(object):

    def __init__(self, defence=0, mana=500, hp=50):
        self.mana = mana
        self.defence = defence 
        self.hp = hp 
        self.used = 0
        self.spells = []
        self.cooldown = defaultdict(int)
        self.callbacks = []
        self.player = True
        self.attacks = SPELLS

    # Magic Missile costs 53 mana. It instantly does 4 damage.
    # Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    # Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
    # Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
    # Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

    def spell(cost, cooldown=0):
        def cast_spell(spell):
            @wraps(spell)
            def wrapped(caster, target):
                if cost > caster.mana:
                    raise SpellException('Out of mana')
                if caster.cooldown[spell.__name__] > 0:
                    raise SpellException('{} Cooldown {}'.format(spell.__name__,
                        caster.cooldown[spell.__name__]))
                caster.mana -= cost
                caster.used += cost
                caster.tick()
                target.tick()
                if caster.hp > 0:
                    spell(caster, target)
                    caster.spells.append(spell.__name__)
                    caster.cooldown[spell.__name__] = cooldown
            SPELLS.append(wrapped)
            return wrapped
        return cast_spell

    def tick(caster):
        callbacks, caster.callbacks = caster.callbacks, []
        for k, v in caster.cooldown.items():
            caster.cooldown[k] = max(0, v-1)
        for call in callbacks:
            call(caster)

    @spell(53)
    def magic_missle(caster, target):
        target.hp -= 4

    @spell(73)
    def drain(caster, target):
        caster.hp += 2
        target.hp -= 2

    def add_callback(self, callback):
        self.callbacks.append(callback)

    @spell(113, cooldown=6)
    def shield(caster, target):
        caster.defence += 7
        def shield_callback(turns):
            def shield_func(caster):
                if turns > 1:
                    caster.add_callback(shield_callback(turns-1))
                else:
                    caster.defence -= 7
            return shield_func
        caster.add_callback(shield_callback(6))

    @spell(173, cooldown=6)
    def poison(caster, target):
        def poison_callback(turns):
            def poison_func(target):
                target.hp -= 3
                if turns > 1:
                    target.add_callback(poison_callback(turns-1))
            return poison_func
        target.add_callback(poison_callback(6))

    @spell(229, cooldown=5)
    def recharge(caster, target):
        def recharge_callback(turns):
            def recharge_func(caster):
                # old_mana = caster.mana
                caster.mana += 101
                # print("Recharging {}: {} -> {}".format(caster.cooldown['recharge'], old_mana, caster.mana))
                if turns > 1:
                    caster.add_callback(recharge_callback(turns-1))
            return recharge_func
        caster.add_callback(recharge_callback(5))

def test_example_1():
    player = Player(hp=10, mana=250)
    boss = Boss(hp=13, attack=8)
    player.poison(boss)
    assert player.hp == 10 and player.mana == 77
    boss.attacks[0](boss, player)
    assert boss.hp == 10 and player.cooldown['poison'] == 5
    assert player.hp == 2
    player.magic_missle(boss)
    assert boss.hp == 3 and player.mana == 24 and player.cooldown['poison'] == 4
    boss.simple_attack(player)
    assert player.hp == 2 and boss.hp == 0

def test_example_2():
    player = Player(hp=10, mana=250)
    boss = Boss(hp=14, attack=8)
    player.recharge(boss)
    assert player.hp == 10 and player.mana == 21
    boss.simple_attack(player)
    assert player.mana == 122 and player.hp == 2 and player.cooldown['recharge'] == 4
    player.shield(boss)
    assert player.mana == 110 and player.hp == 2 and player.defence == 7
    assert player.cooldown['recharge'] == 3
    boss.simple_attack(player)
    assert player.mana == 211 and player.hp == 1
    assert boss.hp == 14
    assert player.cooldown['recharge'] == 2 and player.cooldown['shield'] == 5
    player.drain(boss)
    assert player.mana == 239 and player.hp == 3
    assert player.cooldown['recharge'] == 1 and player.cooldown['shield'] == 4
    assert boss.hp == 12
    boss.simple_attack(player)
    assert player.mana == 340 and player.hp == 2
    assert player.cooldown['recharge'] == 0 and player.cooldown['shield'] == 3
    assert boss.hp == 12
    player.poison(boss)
    assert player.mana == 167 and player.hp == 2
    assert player.cooldown['poison'] == 6 and player.cooldown['shield'] == 2
    assert player.cooldown['recharge'] == 0
    assert boss.hp == 12
    boss.simple_attack(player)
    assert player.mana == 167 and player.hp == 1 and player.defence == 7
    assert player.cooldown['poison'] == 5 and player.cooldown['shield'] == 1
    assert boss.hp == 9
    player.magic_missle(boss)
    assert player.mana == 114 and player.hp == 1 and player.defence == 0
    assert player.cooldown['poison'] == 4 and player.cooldown['shield'] == 0
    assert boss.hp == 2
    boss.simple_attack(player)
    assert player.mana == 114 and player.hp == 1
    assert player.cooldown['poison'] == 3
    assert boss.hp == -1 

def worth_it(player, boss, min_mana):
    if player.hp <= 0 or boss.hp <= 0:
        return False
    if min_mana is None:
        return True
    if boss.player:
        player, boss = boss, player
    return player.used < min_mana

def part1(player, boss):
    min_mana = None
    queue = [(player, boss)]
    while queue:
        attacker, defender = queue.pop()
        for attack in attacker.attacks:
            a, d = deepcopy(attacker), deepcopy(defender)

            try:
                attack(a, d)
            except SpellException as e:
                continue

            if d.hp <= 0 and not d.player:
                min_mana = min(min_mana or a.used, a.used)
            if worth_it(a, d, min_mana):
                x, y = a, d
                if d.player:
                    y, x = x, y
                print('{} {:4s} Boss: {:2} Player: {:2} {:3} {}'.format(
                    'B' if d.player else 'P', str(min_mana), y.hp,
                    x.hp, x.mana,','.join(x.spells)))
                queue.append((d, a))
    return min_mana

def part2(player, boss):
    min_mana = None
    queue = [(player, boss)]
    while queue:
        attacker, defender = queue.pop()
        for attack in attacker.attacks:
            a, d = deepcopy(attacker), deepcopy(defender)

            if a.player:
                a.hp -= 1

            if a.hp > 0:
                try:
                    attack(a, d)
                except SpellException as e:
                    continue

            if (d.hp <= 0 and a.player) or (a.hp <= 0 and d.player):
                if d.hp <=0 and a.hp <= 0:
                    print("Both dead")
                if d.player:
                    a = d
                min_mana = min(min_mana or a.used, a.used)
            if worth_it(a, d, min_mana):
                queue.append((d, a))
                swap = False
                if d.player:
                    swap = True
                    a, d = d, a
                # print('{} {:4s} Boss: {:2} Player: {:2} {:3} {}'.format(
                #     'B' if swap else 'P', str(min_mana), d.hp,
                #     a.hp, a.mana,','.join(a.spells)))
    return min_mana

def parse(text):
    boss = {'Hit Points': None, 'Damage': None}
    for line in text.splitlines():
        if line == '':
            continue
        k, v = line.split(': ')
        boss[k] = int(v)
    return Boss(hp=boss['Hit Points'], attack=boss['Damage']), Player()

if __name__ == '__main__':
    boss, player = parse(get_input(day=22, year=2015))
    # print("Part 1: {}".format(part1(player, boss)))
    # Not 1309,1295
    print("Part 2: {}".format(part2(player, boss)))
