# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
#
#   This file is part of pyherc.
#
#   pyherc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyherc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Dictionary for behaviour driven tests
"""

from hamcrest.core.base_matcher import BaseMatcher
from mockito import mock, when
from pyherc.data.effects import DamageEffect, Heal, Poison
from pyherc.data.geometry import find_direction
from pyherc.rules import (attack, cast, drop_item, Dying, gain_domain,
                          is_move_legal, move, wait)
from pyherc.test.builders import (ActionFactoryBuilder, EffectsFactoryBuilder,
                                  LevelBuilder, SpellCastingFactoryBuilder,
                                  SpellGeneratorBuilder)


def add_history_value(character, attribute):
    """
    Add given value into history data of the character

    :param character: Character to modify
    :type character: Character
    :param attribute: name of the attribute to store
    :type attribute: String

    .. versionadded:: 0.10
    """
    if not hasattr(character, 'old_values'):
        character.old_values = {}

    if hasattr(getattr(character, attribute), 'copy'):
        character.old_values[attribute] = getattr(character, attribute).copy()
    else:
        character.old_values[attribute] = getattr(character, attribute)


def get_history_value(character, attribute):
    """
    Get given history value

    :param character: character whose history value to get
    :type character: Character
    :param attribute: name of the attribute
    :type attribute: String
    :returns: old value of the attribute

    .. versionadded:: 0.10
    """
    return character.old_values[attribute]


def Level():
    """
    Creates a level

    :returns: fully initialised level
    :rtype: Level
    """
    level = (LevelBuilder()
             .build())
    return level


class LevelLocation():
    """
    Defines a location in game world
    """
    def __init__(self, level, location):
        """
        Default constructor

        :param level: level where location is
        :type level: Level
        :param location: location within level
        :type location: (int, int)
        """
        super().__init__()
        self.level = level
        self.location = location

    def __str__(self):
        """
        Create string representation of location
        """
        return 'level: {0}, location: {1}'.format(self.level,
                                                  self.location)


def place(character, location):
    """
    Place character to given location

    :param character: character to place
    :type character: Character
    :param location: location to place the character
    :type location: LevelLocation
    """
    location.level.add_creature(character, location.location)


def middle_of(level):
    """
    Find out middle point of level

    :param level: level to inspect
    :type level: Level
    :returns: middle point of level
    :rtype: (int, int)
    """
    x_loc = level.get_size()[0] // 2
    y_loc = level.get_size()[1] // 2
    location = LevelLocation(level, (x_loc, y_loc))

    return location


def right_of(object):
    """
    Find location on the right side of something

    :param object: entity on map
    :type object: Item or Creature
    :returns: point right of the entity
    :rtype: (int, int)
    """
    x_loc = object.location[0] + 1
    y_loc = object.location[1]
    location = LevelLocation(object.level, (x_loc, y_loc))

    return location


def make(actor, action):
    """
    Trigger an action

    :param actor: actor doing the action
    :type actor: Character
    :param action: action to perfrom
    """
    action(actor)


class Wait():
    """
    Class representing waiting a bit
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def __call__(self, character):
        """
        Performs waiting

        :param character: character waiting
        :type character: Character
        """
        add_history_value(character, 'tick')

        action_factory = (ActionFactoryBuilder()
                          .with_wait_factory()
                          .build())

        wait(character, action_factory)


def wait_():
    """
    Wait a bit
    """
    action = Wait()
    return action


class TakeRandomStep():
    """
    Class representing taking a random step
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def __call__(self, character):
        """
        Performs taking a single step

        :param character: character walking
        :type character: Character
        """
        add_history_value(character, 'tick')

        action_factory = (ActionFactoryBuilder()
                          .with_move_factory()
                          .build())

        directions = [direction for direction in range(1, 9)
                      if is_move_legal(character,
                                       direction,
                                       'walk',
                                       action_factory)]

        assert len(directions) > 0

        move(character=character,
             direction=directions[0],
             action_factory=action_factory)


def take_random_step():
    """
    Take a single step
    """
    return TakeRandomStep()


class CastSpell():
    """
    Class representing casting a spell
    """
    def __init__(self, spell_name, target=None):
        """
        Default constructor

        :param spell_name: name of the spell to cast
        :type spell_name: string
        :param target: target of the spell
        :type target: Character
        """
        super().__init__()
        self.spell_name = spell_name
        self.target = target

    def __call__(self, caster):
        """
        Performs the casting

        :param caster: character doing the casting
        :type caster: Character
        """
        add_history_value(caster, 'hit_points')

        spell_factory = SpellGeneratorBuilder().build()

        effects_factory = (EffectsFactoryBuilder()
                           .with_effect('heal medium wounds',
                                        {'type': Heal,
                                         'duration': None,
                                         'frequency': None,
                                         'tick': 0,
                                         'healing': 10,
                                         'icon': None,
                                         'title': 'Heal medium wounds',
                                         'description': 'Heals medium amount of damage'})  # noqa
                           .with_effect('cause wound',
                                        {'type': DamageEffect,
                                         'duration': None,
                                         'frequency': None,
                                         'tick': 0,
                                         'damage': 5,
                                         'damage_type': 'magic',
                                         'icon': None,
                                         'title': 'Cause minor wound',
                                         'description': 'Causes minor amount of damage'})  # noqa
                           .with_effect('fire',
                                        {'type': DamageEffect,
                                         'duration': 30,
                                         'frequency': 5,
                                         'tick': 0,
                                         'damage': 3,
                                         'damage_type': 'fire',
                                         'icon': None,
                                         'title': 'Fire',
                                         'description': 'You are on fire!'})
                           .build())

        spell_casting_factory = (SpellCastingFactoryBuilder()
                                 .with_spell_factory(spell_factory)
                                 .with_effects_factory(effects_factory)
                                 .build())

        action_factory = (ActionFactoryBuilder()
                          .with_dying_rules()
                          .with_spellcasting_factory(spell_casting_factory)
                          .build())

        if self.target:
            direction = find_direction(caster.location,
                                       self.target.location)
        else:
            direction = 1

        cast(caster,
             direction=direction,
             spell_name=self.spell_name,
             action_factory=action_factory)


def cast_spell(spell_name, target=None):
    """
    Cast a spell

    :param spell_name: name of the spell to cast
    """
    action = CastSpell(spell_name, target)
    return action


class Hit():
    """
    Class representing a hit in unarmed combat
    """
    def __init__(self, target):
        """
        Default constructor

        :param target: target to attack
        """
        super().__init__()
        self.target = target

    def __call__(self, attacker):
        """
        Performs the hit

        :param attacker: character attacking
        :type attacker: Character
        """
        add_history_value(self.target, 'hit_points')

        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        action_factory = (ActionFactoryBuilder()
                          .with_move_factory()
                          .with_attack_factory()
                          .with_drink_factory()
                          .with_inventory_factory()
                          .with_dying_rules()
                          .build())

        attack(attacker,
               find_direction(attacker.location,
                              self.target.location),
               action_factory,
               rng)


def hit(target):
    """
    Hit target

    :param target: target to hit
    :returns: callable action
    """
    action = Hit(target)
    return action


class WieldAction():
    """
    Action to get chracter to wield something
    """
    def __init__(self, weapon):
        """
        Default constructor

        :param weapon: weapon to wield
        :type weapon: Item
        """
        super().__init__()
        self.weapon = weapon

    def __call__(self, character):
        """
        Wield the item

        :param character: character wielding the weapon
        :type character: Character
        """
        character.inventory.weapon = self.weapon
        return character


def wielding(weapon):
    """
    Make a character to wield a weapon
    """
    action = WieldAction(weapon)
    return action


class GainDomainAction():
    """
    Action to gain a domain
    """

    def __init__(self, item, domain):
        """
        Default constructor
        """
        super().__init__()
        self.item = item
        self.domain = domain

    def __call__(self, character):
        """
        Execute the action
        """
        action_factory = (ActionFactoryBuilder()
                          .with_gain_domain_factory()
                          .with_dying_rules()
                          .build())

        gain_domain(character=character,
                    item=self.item,
                    domain=self.domain,
                    action_factory=action_factory)


def gain_domain_(item, domain):
    """
    Gain domain
    """
    return GainDomainAction(item=item,
                            domain=domain)


class HasLessHitPoints(BaseMatcher):
    """
    Matcher for checking that hit points have gone down
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.old_hit_points = None

    def _matches(self, item):
        """
        Check if match

        :param item: match against this item
        """
        self.old_hit_points = get_history_value(item, 'hit_points')

        if self.old_hit_points > item.hit_points:
            return True
        else:
            return False

    def describe_to(self, description):
        """
        Descripe the match

        :param description: description text to append
        :type description: string
        """
        description.append(
            'Character with less than {0} hitpoints'.format(
                self.old_hit_points))

    def describe_mismatch(self, item, mismatch_description):
        """
        Descripe the mismatch

        :item: mismatching item
        :param mismatch_description: description text to append
        :type mismatch_description: string
        """
        mismatch_description.append(
            'Character has {0} hit points'.format(item.hit_points))


def has_less_hit_points():
    """
    Check that hit points have gone down
    """
    return HasLessHitPoints()


def at_(loc_x, loc_y):
    """
    Create a new location entity

    :param loc_x: x-coordinate of location
    :type loc_x: int
    :param loc_y: y-coordinate of location
    :type loc_y: int
    :returns: location
    :rtype: (int, int)
    """
    return (loc_x, loc_y)


def affect(target, effect_spec):
    """
    Triggers an effect on target

    :param target: target of the effect
    :type target: Character
    :param effect_spec: effect specification
    :type effect_spec: {}
    """
    effect_type = effect_spec['effect_type']
    del effect_spec['effect_type']
    effect_spec['target'] = target

    new_effect = effect_type(**effect_spec)

    add_history_value(target, 'hit_points')

    new_effect.trigger(Dying())


def with_(effect_spec):
    """
    Syntactic sugar

    :param effect_spec: effect specification
    :type effect_spec: {}
    :returns: effect specification
    :rtype: {}
    """
    return effect_spec


def potent_poison(target=None):
    """
    Creates effect specification for poison

    :param target: target of the effect
    :type target: Character
    :returns: effect specification
    :rtype: {}
    """
    return {'effect_type': Poison,
            'duration': 1,
            'frequency': 1,
            'tick': 0,
            'damage': 100,
            'target': target,
            'icon': 101,
            'title': 'potent poison',
            'description': 'causes huge amount of damage'}


def weak_poison(target=None):
    """
    Creates effect specification for poison

    :param target: target of the effect
    :type target: Character
    :returns: effect specification
    :rtype: {}
    """
    return {'effect_type': Poison,
            'duration': 1,
            'frequency': 1,
            'tick': 0,
            'damage': 1,
            'target': target,
            'icon': 101,
            'title': 'weak poison',
            'description': 'causes tiny amount of damage'}


class CarryAction():
    """
    Action to get chracter to carry something
    """
    def __init__(self, item):
        """
        Default constructor

        :param item: item to carry
        :type item: Item
        """
        super().__init__()
        self.item = item

    def __call__(self, character):
        """
        Put item in inventory

        :param character: character carrying the item
        :type character: Character
        """
        character.inventory.append(self.item)
        return character


def carrying(item):
    """
    make character to carry an item
    """
    action = CarryAction(item)
    return action


class Drop():
    """
    Class representing dropping an item
    """
    def __init__(self, item):
        """
        Default constructor

        :param item: item to drop
        """
        super().__init__()
        self.item = item

    def __call__(self, actor):
        """
        Performs the drop action

        :param actor: character dropping the item
        :type actor: Character
        """
        add_history_value(actor, 'location')
        add_history_value(actor, 'level')
        add_history_value(actor, 'inventory')
        add_history_value(actor, 'tick')

        action_factory = (ActionFactoryBuilder()
                          .with_move_factory()
                          .with_attack_factory()
                          .with_drink_factory()
                          .with_inventory_factory()
                          .build())

        drop_item(actor,
                  self.item,
                  action_factory)


def drop(item):
    """
    make chracter to drop an item
    """
    action = Drop(item)
    return action


class HasDropped(BaseMatcher):
    """
    Matcher for checking that item has been dropped
    """
    def __init__(self, item):
        """
        Default constructor
        """
        super().__init__()
        self.item = item
        self.fail_reason = ''

    def _matches(self, item):
        """
        Check if match

        :param item: match against this item
        """
        if self.item in item.inventory:
            self.fail_reason = 'item not dropped'
            return False

        if self.item.level is None:
            self.fail_reason = 'item in limbo'
            return False

        if self.item.location != item.location:
            self.fail_reason = 'item dropped to incorrect location'
            return False

        if not self.item in self.item.level.items:
            self.fail_reason = 'item not in level'
            return False

        self.old_time = get_history_value(item, 'tick')
        self.new_time = item.tick
        if not self.old_time < self.new_time:
            self.fail_reason = 'time did not pass'
            return False

        return True

    def describe_to(self, description):
        """
        Descripe the match

        :param description: description text to append
        :type description: string
        """
        description.append('Character who dropped {0}'
                           .format(self.item.name))

    def describe_mismatch(self, item, mismatch_description):
        """
        Descripe the mismatch

        :item: mismatching item
        :param mismatch_description: description text to append
        :type mismatch_description: string
        """
        if self.fail_reason == 'item not dropped':
            mismatch_description.append('{0} is still holding {1}'
                                        .format(item,
                                                self.item))
        elif self.fail_reason == 'item in limbo':
            mismatch_description.append('{0} is not in any level'
                                        .format(self.item))
        elif self.fail_reason == 'item dropped to incorrect location':
            mismatch_description.append('{0} dropped to {1}, should been {2}'
                                        .format(self.item,
                                                self.item.location,
                                                item.location))
        elif self.fail_reason == 'item not in level':
            mismatch_description.append('{0} is not in level {1}'
                                        .format(self.item,
                                                self.item.level))
        elif self.fail_reason == 'time did not pass':
            mismatch_description.append(
                'Flow of time is incorrect. Before: {0}, after: {1}'
                .format(self.old_time,
                        self.new_time))
        else:
            mismatch_description.append('Unimplemented matcher')


def has_dropped(item):
    """
    Check if character has dropped item
    """
    return HasDropped(item)
