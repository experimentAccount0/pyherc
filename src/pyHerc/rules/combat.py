#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

import logging
from pyHerc.rules import tables
from pyHerc.rules import utils
from pyHerc.rules import time
from pyHerc.data.model import Damage
import random

__logger = logging.getLogger('pyHerc.rules.combat')

def meleeAttack(model, attacker, target, dice = []):
    """
    Perform single round of attacking in melee
    @param model: model of the world
    @param attacker: character attacking
    @param target: target of the attack
    @param dice: prerolled dice
    """
    assert(model != None)
    assert(attacker != None)
    assert(target != None)
    assert(dice != None)

    event = {}
    event['type'] = 'melee'
    event['attacker'] = attacker
    event['target'] = target
    event['location'] = attacker.location
    event['level'] = attacker.level

    __logger.debug(attacker.__str__() + ' is attacking ' + target.__str__())
    hit = checkHitInMelee(model, attacker, target, dice)

    event['hit'] = hit

    if hit:
        __logger.debug('attack hits')
        damage = getDamageInMelee(model, attacker, target, dice)

        if damage < 1:
            damage = 1
        __logger.debug('attack does ' + damage.amount.__str__() + ' points of damage')
        event['damage'] = damage
        #TODO: resistances
        target.hp = target.hp - damage.amount
        __logger.debug(target.__str__() + ' has ' + target.hp.__str__() + ' hp left')
        model.raiseEvent(event)

        if target.hp <= 0:
            __logger.debug(target.__str__() + ' has died')
            event = {}
            event['type'] = 'death'
            event['character'] = target
            event['location'] = target.location
            event['level'] = target.level
            model.raiseEvent(event)
            #TODO: implement leaving corpse
            if target != model.player:
                target.level.removeCreature(target)
            else:
                model.endCondition = 1
    else:
        __logger.debug('attack misses')
        model.raiseEvent(event)

    attacker.tick = time.getNewTick(attacker, 6)

def checkHitInMelee(model, attacker, target, dice = []):
    """
    Checks if attacker hits target
    @param attacker: character attacking
    @param target: target of the attack
    @param dice: optional prerolled dice
    """
    assert(model != None)
    assert(attacker != None)
    assert(target != None)
    assert(dice != None)

    ac = getArmourClass(model, target)
    if len(dice) > 0:
        attackRoll = dice.pop() + getMeleeAttackBonus(model, attacker)
    else:
        attackRoll = random.randint(1, 20) + getMeleeAttackBonus(model, attacker)

    if attackRoll >= ac:
        return 1
    else:
        return 0

def getDamageInMelee(model, attacker, target, dice = []):
    """
    Gets damage done in melee
    @param model: model of the world
    @param attacker: character attacking
    @param target: target of the attack
    @param dice: optional prerolled dice
    """
    assert(model != None)
    assert(attacker != None)
    assert(target != None)
    assert(dice != None)

    damage = Damage()

    if len(attacker.weapons) > 0:
        #use weapon in close combat attack
        attackDice = attacker.weapons[0].damage
    else:
        #attack with bare hands
        attackDice = attacker.attack

    if len(dice) > 0:
        damageRoll = dice.pop()
        assert(damageRoll <= utils.getMaxScore(attackDice))
    else:
        damageRoll = utils.rollDice(attackDice)

    if len(attacker.weapons) > 0:
        weapon = attacker.weapons[0]
        if 'light weapon' in weapon.tags:
            #light weapons get only 1 * str bonus when wielded two-handed
            damage.amount = damageRoll + getAttributeModifier(model, attacker, 'str')
            damage.type = weapon.damageType
        else:
            #all other melee weapons get 1.5 * str bonus when wielded two-handed
            damage.amount = damageRoll + getAttributeModifier(model, attacker, 'str') * 1.5
            damage.type = weapon.damageType
    else:
        #unarmed combat get only 1 * str bonus
        damage.amount = damageRoll + getAttributeModifier(model, attacker, 'str')
        damage.type = 'bludgeoning'

    damage.amount = int(round(damage.amount))
    return damage

def getMeleeAttackBonus(model, character):
    """
    Get attack bonus used in melee
    @param model: model of the world
    @param character: character whose attack bonus should be calculated
    @return: Attack bonus
    """
    return  getAttributeModifier(model, character, 'str') + getSizeModifier(model, character)

def getArmourClass(model, character):
    """
    Get armour class of character
    @param model: model of the world
    @param character: character whose armour class should be calculated
    @return: Armour class
    """
    return 10 + getSizeModifier(model, character) + getAttributeModifier(model, character, 'dex')

def getAttributeModifier(model, character, attribute):
    """
    Get attribute modifier
    @param model: model of the world
    @param character: character whose attribute modifier should be calculated
    @param attribute: attribute to check
    @note: valid attributes are: str, dex
    @return: Attribute modifier
    """
    assert(model != None)
    assert(character != None)

    if attribute == 'str':
        return model.tables.attributeModifier[character.str]
    elif attribute == 'dex':
        return model.tables.attributeModifier[character.dex]

def getSizeModifier(model, character):
    """
    Get size modifier for character
    @param model: model of the world
    @param character: character whose size modifier should be calculated
    """
    assert(model != None)
    assert(character != None)

    return model.tables.sizeModifier[character.size]
