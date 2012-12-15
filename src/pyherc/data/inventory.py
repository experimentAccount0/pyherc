#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for Inventory related classes
"""

from pyherc.aspects import logged

class Inventory(object):
    """
    Represents an inventory of items
    """
    @logged
    def __init__(self):
        """
        Default constructor
        """
        super(Inventory, self).__init__()

        self.__items = []

        self.__ring = None
        self.__weapon = None
        self.__gloves = None
        self.__boots = None
        self.__belt = None
        self.__helm = None
        self.__necklace = None
        self.__projectiles = None
        self.__shield = None
        self.__armour = None

    def __len__(self):
        """
        Length of the container
        """
        return len(self.__items)

    def __getitem__(self, key):
        """
        Access an item in Inventory
        """
        return self.__items.__getitem__(key)

    def __setitem__(self, key, value):
        """
        Set item in inventory
        """
        self.__items.__setitem__(key, value)

    def __delitem__(self, key):
        """
        Delete item from inventory
        """
        item = self.__items[key]
        self.remove(item)

    def __iter__(self):
        """
        Get iterator for content of inventory
        """
        return self.__items.__iter__()

    def append(self, item):
        """
        Append an item into inventory
        """
        self.__items.append(item)

    def remove(self, item):
        """
        Remove item from inventory

        :param item: item to remove
        :type item: Item
        """
        self.__items.remove(item)

        if item == self.weapon:
            self.weapon = None

    def __get_weapon(self):
        """
        Weapon currently in use
        """
        return self.__weapon

    def __set_weapon(self, weapon):
        """
        Weapon currently in use
        """
        self.__weapon = weapon

    def _repr_pretty_(self, p, cycle):
        """
        Pretty print for IPython

        :param p: printer to write
        :param cycle: has pretty print detected a cycle?
        """
        if cycle:
            p.text('Inventory(...)')
        else:
            p.text('Inventory:')
            for item in self.__items:
                p.pretty(item)
                p.breakable()

    weapon = property(__get_weapon, __set_weapon)