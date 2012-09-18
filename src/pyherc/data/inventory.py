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

from pyherc.aspects import Logged

class Inventory(object):
    """
    Represents an inventory of items
    """
    logged = Logged()

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
        self.__items.__delitem__(key)

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