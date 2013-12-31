# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Public interface for combat rules
"""

from pyherc.aspects import log_info, log_debug
from pyherc.rules.public import ActionParameters

#@guarded_action
@log_info
def attack(self, direction, action_factory, rng):
    """
    Attack to given direction

    :param direction: direction to attack
    :type direction: integer
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory
    :param rng: random number generator
    :type rng: Random
    """
    if self.inventory.weapon != None:
        weapon = self.inventory.weapon.weapon_data
        if self.inventory.projectiles != None:
            ammunition = self.inventory.projectiles.ammunition_data
        else:
            ammunition = None
    else:
        weapon = None

    if weapon == None:
        attack_type = 'unarmed'
    else:
        if (ammunition == None or
                weapon.ammunition_type != ammunition.ammunition_type):
            attack_type = 'melee'
        else:
            target_loc = self.get_location_at_direction(direction)
            if self.level.get_creature_at(target_loc) == None:
                if self.level.blocks_movement(target_loc[0], target_loc[1]):
                    attack_type = 'melee'
                else:
                    attack_type = 'ranged'
            else:
                attack_type = 'melee'

    action = action_factory.get_action(
                        AttackParameters(
                            attacker = self,
                            direction = direction,
                            attack_type = attack_type,
                            random_number_generator = rng))

    action.execute()

class AttackParameters(ActionParameters):
    """
    Object for controlling attack action creation
    """

    @log_debug
    def __init__(self, attacker, direction, attack_type,
                 random_number_generator):
        """
        Construct AttackParameters

        Args:
            attacker: Character doing an attack
            direction: Direction to attack to
            attack_type: type of attack to perform
            random_number_generator: Random number generator to use
        """
        ActionParameters.__init__(self)

        self.action_type = 'attack'
        self.attacker = attacker
        self.direction = direction
        self.attack_type = attack_type
        self.random_number_generator = random_number_generator
        self.model = None

    @log_debug
    def __str__(self):
        """
        Get string representation of this object
        """
        return 'attack with attack type of ' + self.attack_type