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
import random

__logger = logging.getLogger('pyHerc.rules.combat')

def meleeAttack(model, attacker, target, dice = []):
    """
    Perform single round of attacking in melee
    Parameters:
        model : model of the world
        attacker : character attacking
        target : target of the attack
        dice : prerolled dice
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
        __logger.debug('attack does ' + damage.__str__() + ' points of damage')
        event['damage'] = damage
        target.hp = target.hp - damage
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
    Parameters:
        attacker : character attacking
        target : target of the attack
        dice : optional prerolled dice
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
    Parameters
        model : model of the world
        attacker : character attacking
        target : target of the attack
        dice : optional prerolled dice
    """
    assert(model != None)
    assert(attacker != None)
    assert(target != None)
    assert(dice != None)

    if len(dice) > 0:
        damageRoll = dice.pop()
    else:
        damageRoll = utils.rollDice(attacker.attack)

    return damageRoll + getAttributeModifier(attacker, 'str')

def getMeleeAttackBonus(model, character):
    """
    Get attack bonus used in melee
    Parameters
        model : model of the world
        character : character whose attack bonus should be calculated
    Returns
        Attack bonus
    """
    #Base attack bonus + Strength modifier + size modifier
    #TODO: take base attack bones into account
    return getAttributeModifier(character, 'str') + getSizeModifier(character)

def getArmourClass(model, character):
    """
    Get armour class of character
    Parameters
        model : model of the world
        character : character whose armour class should be calculated
    Returns
        Armour class
    """
    return 10 + getSizeModifier(character) + getAttributeModifier(character, 'dex')

def getAttributeModifier(character, attribute):
    """
    Get attribute modifier
    Parameter:
        character : character whose attribute modifier should be calculated
        attribute : attribute to check
                        str, dex
    Returns:
        Attribute modifier
    """
    tables.loadTables()

    if attribute == 'str':
        return tables.attributeModifier[character.str]
    elif attribute == 'dex':
        return tables.attributeModifier[character.dex]

def getSizeModifier(character):
    """
    Get size modifier for character
    Parameters:
        character : character whose size modifier should be calculated
    """
    assert(character != None)

    tables.loadTables()
    return tables.sizeModifier[character.size]

