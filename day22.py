#!/usr/bin/env python3

from get_input import get_input
from collections import defaultdict
from copy import deepcopy

class Boss(object):
    def __init__(self, attack, defence, hp):
        self.hp = hp
        self.defence = defence
        self.attack = attack
        self.is_player = False

    def clone(self):
        yield deepcopy(self)

class Player(object):
    def __init__(self, hp=50, mana=500):
        self._mana = mana
        self.mana_used = 0
        self.hp = hp
        self.is_player = True
        self._timers = defaultdict(int)
        self._attack = None
        self._actions = [self.magic_missle]

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value):
        if value < 0:
            raise ValueError("Not enough mana {}".format(value))
        self.mana_used += max(self._mana - value, 0)
        self._mana = value

    @property
    def defence(self):
        return 0
    
    @property
    def attack(self):
        return 0 

    def magic_missle(self):
        self.mana -= 53
        return 4

    def drain(self):
        self.mana -= 73
        self.hp += 2
        return 2

    @self.timer(6)
    def shield(self):
        self.mana -= 113
        return 0

    @self.timer(6)
    def poison(self):
        self.mana -= 173
        return 3

    @self.timer(5)
    def recharge(self):
        self.mana -= 229
        return 0

    def clone(self):
        for action in self._actions: 
            copy = deepcopy(self)
            copy.timers = {k: max(v-1, 0) for k, v in copy._timers.items()}
            copy._attack = action
            yield copy

def part1(player, boss):
    queue = [(player, boss)]
    min_mana = None
    while queue:
        attacker, defender = queue.pop()
        defender.hp -= max(attacker.attack - defender.defence, 1)
        if defender.hp <= 0 and not defender.is_player:
            min_mana = min(min_mana or defender.mana_used, defender.mana_used)
        elif 0 < defender.hp:
            for clone in attacker.clone():
                queue.append((defender, clone))
    return min_mana

def part2(player, boss):
    pass

def parse(text):
    boss_stats = dict(line.split(': ') for line in text.splitlines())
    boss = Boss(defence=0,
            attack=int(boss_stats['Damage']),
            hp=int(boss_stats['Hit Points']))
    return boss, Player()

if __name__ == '__main__':
    boss, player = parse(get_input(day=22, year=2015))
    print("Part 1: {}".format(part1(player, boss)))
    print("Part 2: {}".format(part2(player, boss)))
