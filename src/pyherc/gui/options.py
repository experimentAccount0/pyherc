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

"""
Module for options menu related functionality
"""

import logging
import images
import pyherc
import pgu.gui
import pygame

class OptionsMenu(pgu.gui.Container):
    """
    Start menu
    """

    def __init__(self,  application, screen, surface_manager, **params):
        """
        Initialises start menu

        Args:
            application: instance of currently running application
            screen: display to draw onto
        """
        super(OptionsMenu, self).__init__(**params)

        self.running = 1
        self.selection = 0
        self.application = application
        self.screen = screen
        self.surface_manager = surface_manager

        self.set_layout()

    def set_layout(self):
        """
        Set layout of this screen
        """
        bg = pgu.gui.Image(
                self.surface_manager.get_image(
                        images.image_start_menu))
        self.add(bg, 0, 0)

        b = pgu.gui.Button("Back", width=150)
        self.add(b, 325, 350)
        b.connect(pgu.gui.CLICK, self.__back_to_start_menu)

    def __back_to_start_menu(self):
        """
        Return back to start menu
        """
        self.application.change_state('start menu')

