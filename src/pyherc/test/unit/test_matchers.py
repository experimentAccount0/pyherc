# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for testing customer matchers
"""

from hamcrest import assert_that, equal_to, has_length, is_
from pyherc.data import Model, wall_tile
from pyherc.data.effects import EffectHandle, EffectsCollection
from pyherc.test.matchers.effect_collection import ContainsEffectHandle
from pyherc.test.matchers.map_connectivity import MapConnectivity
from pyherc.test.builders import LevelBuilder


class TestLevelConnectivity():
    """
    Class for testing level connectivity matcher
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.matcher = None
        self.wall_empty = None
        self.floor_rock = None
        self.wall_ground = None

    def setup(self):
        """
        Setup the tests
        """
        self.wall_empty = None
        self.floor_rock = 2
        self.wall_ground = 3
        self.level = (LevelBuilder()
                      .with_size((20, 10))
                      .with_floor_tile(self.floor_rock)
                      .with_wall_tile(self.wall_ground)
                      .build())
        self.matcher = MapConnectivity()

    def test_unconnected_level(self):
        """
        Test that unconnected level is reported correctly
        """
        for loc_x in range(2, 5):
            wall_tile(self.level, (loc_x, 2), self.wall_empty)
            wall_tile(self.level, (loc_x, 5), self.wall_empty)

        assert_that(self.matcher._matches(self.level), is_(equal_to(False)))

    def test_connected_level(self):
        """
        Test that connected level is reported correctly
        """
        for loc_x in range(2, 8):
            wall_tile(self.level, (loc_x, 3), self.wall_empty)
            wall_tile(self.level, (loc_x, 6), self.wall_empty)
            wall_tile(self.level, (5, loc_x), self.wall_empty)

        assert_that(self.matcher._matches(self.level), is_(equal_to(True)))

    def test_that_all_points_are_found(self):
        """
        Test that connectivity can find all open points
        """
        wall_tile(self.level, (0, 0), self.wall_empty)
        wall_tile(self.level, (5, 5), self.wall_empty)
        wall_tile(self.level, (20, 10), self.wall_empty)

        points = self.matcher.get_all_points(self.level, self.wall_empty)

        assert_that(points, has_length(3))

    def test_that_open_corners_work(self):
        """
        Test that finding connectivity with open corners work
        """
        wall_tile(self.level, (0, 0), self.wall_empty)
        wall_tile(self.level, (20, 0), self.wall_empty)
        wall_tile(self.level, (0, 10), self.wall_empty)
        wall_tile(self.level, (20, 10), self.wall_empty)

        assert_that(self.matcher._matches(self.level), is_(equal_to(False)))

    def test_that_convoluted_case_works(self):
        """
        Test a convoluted case with 3 open areas and 2 of them being connected
        to border
        """
        self.level = (LevelBuilder()
                      .with_size((10, 10))
                      .with_floor_tile(self.floor_rock)
                      .with_wall_tile(self.wall_ground)
                      .build())

        wall_tile(self.level, (2, 5), self.wall_empty)
        wall_tile(self.level, (2, 6), self.wall_empty)
        wall_tile(self.level, (2, 7), self.wall_empty)
        wall_tile(self.level, (2, 8), self.wall_empty)
        wall_tile(self.level, (2, 9), self.wall_empty)
        wall_tile(self.level, (2, 10), self.wall_empty)

        wall_tile(self.level, (5, 8), self.wall_empty)

        wall_tile(self.level, (5, 2), self.wall_empty)
        wall_tile(self.level, (6, 2), self.wall_empty)
        wall_tile(self.level, (7, 2), self.wall_empty)
        wall_tile(self.level, (8, 2), self.wall_empty)
        wall_tile(self.level, (9, 2), self.wall_empty)
        wall_tile(self.level, (10, 2), self.wall_empty)

        all_points = self.matcher.get_all_points(self.level, self.wall_empty)
        connected_points = self.matcher.get_connected_points(self.level,
                                                all_points[0],
                                                self.wall_empty,
                                                [])

        assert_that(self.matcher._matches(self.level), is_(equal_to(False)))

class TestContainsEffectHandle():
    """
    Tests for ContainsEffectHandle matcher
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_match_single_handle(self):
        """
        Test that single handle can be matched
        """
        collection = EffectsCollection()
        handle = EffectHandle(trigger = 'on drink',
                              effect = None,
                              parameters = None,
                              charges = 1)

        collection.add_effect_handle(handle)

        matcher = ContainsEffectHandle(handle)

        assert_that(matcher._matches(collection), is_(equal_to(True)))

    def test_detect_sinle_mismatch(self):
        """
        Test that missing a single handle is detected correctly
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)

        handle2 = EffectHandle(trigger = 'on kick',
                               effect = None,
                               parameters = None,
                               charges = 1)

        matcher = ContainsEffectHandle(handle2)

        assert_that(matcher._matches(collection), is_(equal_to(False)))

    def test_match_multiple_handles(self):
        """
        Test that matcher can match multiple handlers
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        handle2 = EffectHandle(trigger = 'on kick',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)
        collection.add_effect_handle(handle2)

        matcher = ContainsEffectHandle([handle1, handle2])

        assert_that(matcher._matches(collection), is_(equal_to(True)))

    def test_detect_mismatch_in_collection(self):
        """
        Test that matcher can detect a mismatch in collection
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        handle2 = EffectHandle(trigger = 'on kick',
                               effect = None,
                               parameters = None,
                               charges = 1)

        handle3 = EffectHandle(trigger = 'on burn',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)
        collection.add_effect_handle(handle2)

        matcher = ContainsEffectHandle([handle1, handle2, handle3])

        assert_that(matcher._matches(collection), is_(equal_to(False)))

    def test_mismatch_any(self):
        """
        Test that matcher can mismatch to any handle
        """
        collection = EffectsCollection()

        matcher = ContainsEffectHandle(None)

        assert_that(matcher._matches(collection), is_(equal_to(False)))

    def test_match_any(self):
        """
        Test that matcher can match to any handle
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)

        matcher = ContainsEffectHandle(None)

        assert_that(matcher._matches(collection), is_(equal_to(True)))
