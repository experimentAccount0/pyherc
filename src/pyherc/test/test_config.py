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
Module for testing main configuration
"""

#pylint: disable=W0614
import os.path
from pyherc.config import Configuration
from pyDoubles.framework import empty_stub #pylint: disable=F0401, E0611
from hamcrest import *

class TestMainConfiguration():
    """
    Tests for main configuration
    """
    def __init__(self):
        """
        Default constructor
        """
        self.config = None

    def setup(self):
        """
        Setup test case
        """
        search_directory = '.'
        current = os.path.normpath(os.path.join(os.getcwd(), search_directory))

        while not os.path.exists(os.path.join(current, 'resources')):
            search_directory = search_directory +'/..'
            current = os.path.normpath(os.path.join(os.getcwd(),
                                                    search_directory))

        base_path = os.path.join(current, 'resources')

        self.config = Configuration(base_path, empty_stub())
        self.config.initialise()

    def test_initialisation(self):
        """
        Test that main configuration can be read and initialised properly

        Note:
            This test reads configuration from resources directory
        """
        config = self.config
        assert_that(config.resolution, is_(not_none()))
        assert_that(config.resolution, is_(not_none()))
        assert_that(config.full_screen, is_(not_none()))
        assert_that(config.caption, is_(not_none()))
        assert_that(config.surface_manager, is_(not_none()))
        assert_that(config.action_factory, is_(not_none()))
        assert_that(config.base_path, is_(not_none()))
        assert_that(config.item_generator, is_(not_none()))
        assert_that(config.creature_generator, is_(not_none()))
        assert_that(config.level_generator_factory, is_(not_none()))
        assert_that(config.tables, is_(not_none()))
        assert_that(config.level_size, is_(not_none()))
        assert_that(config.base_path, is_(not_none()))
        assert_that(config.model, is_(not_none()))
        assert_that(config.rng, is_(not_none()))
