#!/usr/bin/env python
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
Module for inventory screen
"""

from pyherc.aspects import logged
from herculeum.ui.controllers import InventoryController

class InventoryScreen(object):
    """
    Class for displaying inventero screen

    .. versionadded:: 0.9
    """
    @logged
    def __init__(self, character, config, screen, action_factory,
                 parent):
        """
        Default constructor
        """
        super(InventoryScreen, self).__init__()

        self.character = character
        self.config = config
        self.screen = screen.subwin(20, 75, 2, 2)
        self.inventory_controller = InventoryController(character,
                                                        action_factory)
        self.parent = parent

        self.keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D']

    @logged
    def _draw_screen(self):
        """
        Update the screen
        """
        self.screen.clear()
        self.screen.border()

        for index, item in enumerate(self.character.inventory):
            if index < 15:
                column = 1
                row = 1 + index
            else:
                column = 37
                row = 1 + index - 15

            self.screen.addstr(1 + index, 1,
                               '{0} {1}'.format(self.keys[index],
                                                item.get_name(self.character,
                                                              True)))

        self.screen.refresh()

    @logged
    def show(self):
        """
        Show inventory screen
        """
        running = 1
        self._draw_screen()

        while running == 1:
            item = None
            key = chr(self.screen.getch())
            if key in ['u', 'r', 'd']:
                self.screen.addstr(0, 2, 'select item')
                item_key = chr(self.screen.getch())
                if item_key in self.keys:
                    index = self.keys.index(item_key)
                    if index < len(self.character.inventory):
                        item = self.character.inventory[index]

                if item != None:
                    if key == 'u':
                        self.inventory_controller.use_item(item)
                    elif key == 'r':
                        self.inventory_controller.unequip_item(item)
                    elif key == 'd':
                        self.inventory_controller.drop_item(item)
            elif key == ' ':
                running = 0

            self._draw_screen()
            self.parent.refresh()