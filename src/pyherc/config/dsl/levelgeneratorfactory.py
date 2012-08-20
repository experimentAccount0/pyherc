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
module for LevelGeneratorFactoryConfig
"""
from pyherc.generators.level.config import LevelGeneratorFactoryConfig

class LevelConfiguration(object):
    """
    DSL for configuring levels
    """

    def __init__(self):
        """
        Default constructor
        """
        super(LevelConfiguration, self).__init__()
        self.room_generators = None
        self.level_partitioners = None
        self.decorators = None
        self.item_adders = None
        self.creature_adders = None
        self.portal_adder_configurations = None
        self.size = None

    def with_rooms(self, rooms):
        """
        Add rooms to configuration

        :param rooms: rooms to use
        :type rooms: [RoomGenerator]
        """
        self.room_generators = rooms
        return self

    def with_partitioners(self, partitioners):
        """
        Add partitioners to configuration

        :param partitioners: partitioners to use
        :type partitioners: [LevelPartitioner]
        """
        self.level_partitioners = partitioners
        return self

    def with_decorators(self, decorators):
        """
        Add decorators to configuration

        :param decorators: decorators to use
        :type decorators: [LevelDecorator]
        """
        self.decorators = decorators
        return self

    def with_items(self, items):
        """
        Add items to configuration

        :param items: items to use
        :type items: [ItemAdder]
        """
        self.item_adders = items
        return self

    def with_creatures(self, creatures):
        """
        Add creatures to configuration

        :param creatures: creatures to use
        :type creatures: [CreatureAdder]
        """
        self.creature_adders = creatures
        return self

    def with_portals(self, portals):
        """
        Add portals to configuration

        :param portals: portals to use
        :type portals: [PortalAdder]
        """
        self.portal_adder_configurations = portals
        return self

    def with_level_size(self, level_size):
        """
        Set level size

        :param level_size: size of level
        :type level_size: (int, int)
        """
        self.size = level_size
        return self

    def build(self):
        """
        Build configuration

        :returns: configuration for level generator factory
        :rtype: LevelGeneratorFactoryConfig
        """
        return LevelGeneratorFactoryConfig(
                room_generators = self.room_generators,
                level_partitioners = self.level_partitioners,
                decorators = self.decorators,
                item_adders = self.item_adders,
                creature_adders = self.creature_adders,
                portal_adder_configurations = self.portal_adder_configurations,
                size = self.size)
