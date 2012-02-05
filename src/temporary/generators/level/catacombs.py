#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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

import logging
import random
import pyherc.generators.item
import pyherc.generators.creature
import pyherc.generators.utils
from pyherc.data.dungeon import Level
from pyherc.data.dungeon import Dungeon
from pyherc.data.dungeon import Portal
from pyherc.data import tiles

class CatacombsLevelGenerator:
    """
    Generator for creating catacombs
    """

    def __init__(self, action_factory):
        self.logger = logging.getLogger('pyherc.generators.level.catacombs.CatacombsLevelGenerator')
        self.item_generator = pyherc.generators.ItemGenerator()
        self.creature_generator = pyherc.generators.CreatureGenerator(action_factory)

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyherc.generators.level.catacombs.CatacombsLevelGenerator')

    def generate_level(self, portal, model, new_portals = 0, level=1, room_min_size = (2, 2)):
        """
        Generate level that starts from given stairs
        @param portal: link new level to this portal
        @param model: model being used
        @param new_portals: amount of portals to generate, default 0
        @param level: changes behaviour of the generator
        @param room_min_size: minimum size for rooms
        """
        self.logger.debug('generating level: ' + level.__str__())
        level_size = model.config['level']['size']
        self.logger.debug('dividing level in sections')
        BSPStack = []
        BSP = pyherc.generators.utils.BSPSection((0, 0), (level_size[0] - 2, level_size[1] - 2), None)
        BSPStack.append(BSP)
        room_stack = []

        temp_level = Level(level_size, tiles.FLOOR_ROCK, tiles.WALL_GROUND)
        #TODO: split into smaller chuncks
        while len(BSPStack) > 0:
            tempBSP = BSPStack.pop()
            tempBSP.split(min_size = (room_min_size[0] + 4, room_min_size[1] + 4))
            if tempBSP.node1 != None:
                BSPStack.append(tempBSP.node1)
            if tempBSP.node2 != None:
                BSPStack.append(tempBSP.node2)
            if tempBSP.node1 == None and tempBSP.node2 == None:
                #leaf
                room_stack.append(tempBSP)

        self.logger.debug('carving rooms')
        for room in room_stack:
            corner1 = (room.corner1[0] + random.randint(1, 4),
                       room.corner1[1] + random.randint(1, 4))
            corner2 = (room.corner2[0] - random.randint(1, 4),
                       room.corner2[1] - random.randint(1, 4))
            self.logger.debug('carving room ' +
                              corner1.__str__() + ':' +
                              corner2.__str__())
            for y in range(corner1[1], corner2[1] + 1):
                for x in range(corner1[0], corner2[0] + 1):
                    temp_level.walls[x][y] = tiles.WALL_EMPTY

        self.logger.debug('carving tunnels')

        area_queue = BSP.getAreaQueue()
        area_queue.reverse()

        while len(area_queue) > 1:
            area1 = area_queue.pop()
            area2 = area_queue.pop()
            center1 = area1.getCenter()
            center2 = area2.getCenter()
            self.logger.debug('carving tunnel between areas '
                              + area1.__str__() + ' and '
                              + area2.__str__())
            self.logger.debug('using center points '
                              + center1.__str__() + ' and '
                              + center2.__str__())
            #connect these two areas
            if area1.direction == 1:
                #areas on top of each other
                if center1[1] < center2[1]:
                    self.logger.debug('tunneling top down ' +
                                    center1[0].__str__() + ':' +
                                    range(center1[1], center2[1]).__str__())
                    for y in range(center1[1], center2[1] + 1):
                        temp_level.walls[center1[0]][y] = tiles.WALL_EMPTY
                else:
                    self.logger.debug('tunneling top down ' +
                                    center1[0].__str__() + ':' +
                                    range(center2[1], center1[1]).__str__())
                    for y in range(center2[1], center1[1] + 1):
                        temp_level.walls[center1[0]][y] = tiles.WALL_EMPTY
            else:
                #areas next to each other
                if center1[0] < center2[0]:
                    self.logger.debug('tunneling sideways ' +
                                    range(center1[0], center2[0]).__str__() +
                                    ':' + center1[1].__str__())
                    for x in range(center1[0], center2[0] + 1):
                        temp_level.walls[x][center1[1]] = tiles.WALL_EMPTY
                else:
                    self.logger.debug('tunneling sideways ' +
                                      range(center2[0], center1[0]).__str__()
                                      + ':' + center1[1].__str__())
                    for x in range(center2[0], center1[0] + 1):
                        temp_level.walls[x][center1[1]] = tiles.WALL_EMPTY

        #decorate dungeon a bit
        temp_walls = []
        for x in range(0, level_size[0] + 1):
            for y in range(0, level_size[1] + 1):
                if temp_level.walls[x][y] != tiles.WALL_EMPTY:
                    if y > 1:
                        temp_walls.append(temp_level.walls[x][y-1])
                        if x > 1:
                            temp_walls.append(temp_level.walls[x-1][y-1])
                        if x < level_size[0]:
                            temp_walls.append(temp_level.walls[x+1][y-1])
                    if y < level_size[1]:
                        temp_walls.append(temp_level.walls[x][y+1])
                        if x > 1:
                            temp_walls.append(temp_level.walls[x-1][y+1])
                        if x < level_size[0]:
                            temp_walls.append(temp_level.walls[x+1][y+1])
                    if x > 1:
                        temp_walls.append(temp_level.walls[x-1][y])
                    if x < level_size[0]:
                        temp_walls.append(temp_level.walls[x+1][y])
                    if tiles.WALL_EMPTY in temp_walls:
                        random_tile = random.randint(1, 100)
                        if random_tile == 98:
                            temp_level.walls[x][y] = tiles.WALL_ROCK_DECO_1
                        elif random_tile == 99:
                            temp_level.walls[x][y] = tiles.WALL_ROCK_DECO_2
                        else:
                            temp_level.walls[x][y] = tiles.WALL_ROCK
                temp_walls = []

        #TODO: more random content creation
        #enter few monsters
        #TODO: more intelligent system to choose monsters
        for i in range(0, 10):
            if level == 1:
                temp_creature = self.creature_generator.generate_creature(
                                            model.tables, {'name':'rat'})
                temp_level.add_creature(temp_creature,
                                            temp_level.find_free_space())
            else:
                temp_creature = self.creature_generator.generate_creature(
                                                model.tables,
                                                {'name':'fire beetle'})
                temp_level.add_creature(temp_creature,
                                        temp_level.find_free_space())

        #throw bunch of food items around
        for i in range(0, 10):
            temp_item = self.item_generator.generateItem(model.tables,
                                                         {'type':'food'})
            temp_item.location = temp_level.find_free_space()
            temp_level.items.append(temp_item)

        for i in range(0, 3):
            temp_item = self.item_generator.generateItem(model.tables,
                                                         {'type':'potion'})
            temp_item.location = temp_level.find_free_space()
            temp_level.items.append(temp_item)

        #throw bunch of weapons around
        for i in range(0, 10):
            temp_item = self.item_generator.generateItem(model.tables,
                                                         {'type':'weapon'})
            temp_item.location = temp_level.find_free_space()
            temp_level.items.append(temp_item)

        if portal != None:
            new_portal = Portal()
            #TODO: refactor for configuration
            new_portal.model = model
            temp_level.add_portal(new_portal,
                                  temp_level.find_free_space(), portal)

        if new_portals > 0:
            for i in range(0, new_portals):
                new_portal = Portal()
                new_portal.model = model
                new_portal.icon = tiles.PORTAL_STAIRS_DOWN
                temp_level.add_portal(new_portal, temp_level.find_free_space())

        # generate next level
        for portal in temp_level.portals:
            if portal.get_other_end() == None:
                if level < 5:
                    #still in catacombs

                    new_level = self.generate_level(portal, model, 1,
                                                   level = level + 1)
                else:
                    #TODO: implement generating dungeon levels
                    pass

        return temp_level