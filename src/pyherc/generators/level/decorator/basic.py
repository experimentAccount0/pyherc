#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
Module for basic decorators
"""

class Decorator(object):
    """
    Super class for level decorators
    """
    def __init__(self, configuration):
        """
        Default constructor

        Args:
            configuration: configuration for decorator
        """
        super(Decorator, self).__init__()
        self.configuration = configuration

    def decorate_level(self, level):
        """
        Decorate level

        Args:
            level: Level to decorate
        """
        pass

class ReplacingDecorator(Decorator):
    """
    Simple decorator used to replace prototiles with real ones
    """
    def __init__(self, configuration):
        """
        Default constructor

        Args:
            configuration: ReplacingDecoratorConfig specifying tiles to replace
        """
        super(ReplacingDecorator, self).__init__(configuration)

    def decorate_level(self, level):
        """
        Decorate level

        Args:
            level: Level to decorate
        """
        floor_keys = self.configuration.ground_config.keys()
        ground_tiles = self.configuration.ground_config
        wall_keys = self.configuration.wall_config.keys()
        wall_tiles = self.configuration.wall_config

        for loc_y in range(len(level.floor[0])):
            for loc_x in range(len(level.floor)):
                proto_tile = level.floor[loc_x][loc_y]
                if proto_tile in floor_keys:
                    level.floor[loc_x][loc_y] = ground_tiles[proto_tile]

                proto_tile = level.walls[loc_x][loc_y]
                if proto_tile in wall_keys:
                    level.walls[loc_x][loc_y] = wall_tiles[proto_tile]


class ReplacingDecoratorConfig(object):
    """
    Configuration for ReplacingDecorator
    """
    def __init__(self):
        """
        Default constructor
        """
        super(ReplacingDecoratorConfig, self).__init__()
        self.ground_config = {}
        self.wall_config = {}

class WallBuilderDecorator(Decorator):
    """
    Decorator used to build walls

    This decorator will search all positions where there are walls next to empty
    space and replace tiles there with specified ones
    """
    def __init__(self, configuration):
        """
        Default constructor

        Args:
            configuration: WallBuilderDecoratorConfig
        """
        super(WallBuilderDecorator, self).__init__(configuration)

    def decorate_level(self, level):
        """
        Decorate level

        Args:
            level: Level to decorate
        """
        for loc_y in range(1, len(level.floor[0]) - 1):
            for loc_x in range(1, len(level.floor) - 1):
                if level.walls[loc_x][loc_y] == self.configuration.empty_tile:
                    self.check_and_replace((loc_x - 1, loc_y), level)
                    self.check_and_replace((loc_x + 1, loc_y), level)
                    self.check_and_replace((loc_x, loc_y - 1), level)
                    self.check_and_replace((loc_x, loc_y + 1), level)
                    self.check_and_replace((loc_x - 1, loc_y - 1), level)
                    self.check_and_replace((loc_x - 1, loc_y + 1), level)
                    self.check_and_replace((loc_x + 1, loc_y - 1), level)
                    self.check_and_replace((loc_x + 1, loc_y + 1), level)

    def check_and_replace(self, location, level):
        """
        Check location and replace tile if it matches configuration

        Args:
            location: (loc_x, loc_y) location to check
            level: Level to use
        """
        loc_x = location[0]
        loc_y = location[1]
        proto_tile = level.walls[loc_x][loc_y]

        if proto_tile in self.configuration.wall_config.keys():
            tile = self.configuration.wall_config[proto_tile]
            level.walls[loc_x][loc_y] = tile

class WallBuilderDecoratorConfig(object):
    """
    Configuration for WallBuilderDecorator
    """
    def __init__(self):
        """
        Default constructor
        """
        super(WallBuilderDecoratorConfig, self).__init__()
        self.wall_config = {}
        self.empty_tile = None

class AggregateDecorator(Decorator):
    """
    Decorator that consists of multiple decorators
    """
    def __init__(self, configuration):
        """
        Default constructor

        Args:
            configuration: AggregateDecoratorConfig
        """
        super(AggregateDecorator, self).__init__(configuration)

    def decorate_level(self, level):
        """
        Decorate level

        Args:
            level: Level to decorate
        """
        for decorator in self.configuration.decorators:
            decorator.decorate_level(level)

class AggregateDecoratorConfig(object):
    """
    Configuration for AggregateDecorator
    """
    def __init__(self):
        """
        Default constructor
        """
        super(AggregateDecoratorConfig, self).__init__()
        self.decorators = []