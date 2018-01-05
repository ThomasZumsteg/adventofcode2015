#!/usr/bin/env python3

from get_input import get_input

class Boss(object):
    def __init__(self, attack, defence, hp):
        self.hp = hp
        self.defence = defence
        self.attack = attack

class Player(object):
    def __init__(self, hp=50, mana=500):
        self._mana = mana
        self._hp = hp
        self._mana_spent = 0
        self._modifiers = 

    def actions(self):
        yield from [self.magic_missle, self.drain, self.shield, 
                self.poison, self.recharg]

    def magic_missle(self):
        self._tick()
        self.mana -= 53
        return 4

    def drain(self):
        self._tick()
        self.mana -= 73
        self.hp += 2
        return 2

    def shield(self):
        self._tick()
        self.mana -= 113
        return 0

    @property
    def defence(self):
        

    @property
    def attack(self):


def fight_gen(player_start, boss_start):
    player, boss = deepcopy(player_start), deepcopy(boss_start)
    attacker, defender = player, boss
    while True:
        defender.hp -= max(attacker.attack - defender.armor, 1)
        yield player, boss

def part1(player, boss):
    pass

def part2(player, boss):
    pass
