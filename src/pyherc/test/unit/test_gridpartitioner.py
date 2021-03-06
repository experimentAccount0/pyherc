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
Tests for GridPartitioner
"""
#pylint: disable=W0614
import random

from hamcrest import (assert_that, equal_to, greater_than, has_length, is_,
                      same_instance)
from mockito import mock, when

from pyherc.generators.level.partitioners import (grid_partitioning,
                                                  RandomConnector)
from pyherc.generators.level.partitioners import (is_connected,
                                                  section_connections,
                                                  mark_neighbours,
                                                  neighbour_sections)
from pyherc.generators.level.partitioners.section import new_section
from pyherc.test.builders import LevelBuilder


class TestGridPartitioner:
    """
    Tests for GridPartitioner
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.partitioner = None
        self.rng = None

    def setup(self):
        """
        Setup tests
        """
        self.level = (LevelBuilder()
                      .with_size((20, 20))
                      .build())
        self.rng = random.Random()
        self.partitioner = grid_partitioning((20, 20), 2, 1, self.rng)

    def test_partitioning_returns_sections(self):
        """
        Test that partitioning level returns default amount of sections
        """
        partitioner = grid_partitioning((20, 20), 3, 3, self.rng)

        sections = partitioner(self.level)

        assert_that(sections, has_length(9))

    def test_sections_have_neighbours(self):
        """
        Test that sections are marked being neighbours
        """
        sections = self.partitioner(self.level)

        assert_that(list(neighbour_sections(sections[0])), 
                    has_length(1))

    def test_new_sections_are_on_level(self):
        """
        Test that created sections are linked to level
        """
        sections = self.partitioner(self.level)

        for section in sections:
            assert_that(section['\ufdd0:level'], is_(same_instance(self.level)))


class TestRandomConnector:
    """
    Tests for RandomConnector class
    """
    def __init__(self):
        """
        Default constructor
        """
        self.connector = None
        self.level = None
        self.rng = None

    def setup(self):
        """
        Setup the test cases
        """
        self.rng = random.Random()
        self.connector = RandomConnector(self.rng)
        self.level = (LevelBuilder().build())

    def test_connect_two_sections(self):
        """
        Test that two adjacent sections can be connected
        """
        section1 = new_section((0, 0), (10, 5), self.level, self.rng)
        section2 = new_section((0, 6), (10, 10), self.level, self.rng)

        mark_neighbours(section1, section2)

        sections = [section1, section2]

        connected_sections = self.connector.connect_sections(sections)

        assert_that(connected_sections[1],
                    is_(equal_to(
                        list(section_connections(connected_sections[0]))[0].connection)))

    def test_connecting_2x2_grid(self):
        """
        Test that 2x2 grid is fully connected
        """
        section00 = new_section((0, 0), (5, 5), self.level, self.rng)
        section10 = new_section((6, 0), (10, 5), self.level, self.rng)
        section01 = new_section((0, 6), (5, 10), self.level, self.rng)
        section11 = new_section((6, 6), (10, 10), self.level, self.rng)

        mark_neighbours(section00, section10)
        mark_neighbours(section00, section01)
        mark_neighbours(section10, section11)
        mark_neighbours(section01, section11)

        sections = [section00, section10, section01, section11]

        connected_sections = self.connector.connect_sections(sections)

        assert_that(connected_sections, has_length(4))

        for section in connected_sections:
            assert_that(list(section_connections(section)),
                        has_length(greater_than(0)))
            assert_that(is_connected(section))

    def test_connect_row_of_sections(self):
        """
        Test special case where connections have to branch

        Row of Sections is connected, starting from the middle
        RandomConnector can not connect this in one path, but has to branch
        """
        section0 = new_section((0, 0), (10, 10), self.level, self.rng)
        section1 = new_section((11, 0), (20, 10), self.level, self.rng)
        section2 = new_section((21, 0), (30, 10), self.level, self.rng)
        section3 = new_section((31, 0), (40, 10), self.level, self.rng)
        section4 = new_section((41, 0), (50, 10), self.level, self.rng)

        mark_neighbours(section0, section1)
        mark_neighbours(section1, section2)
        mark_neighbours(section2, section3)
        mark_neighbours(section3, section4)

        sections = [section0, section1, section2, section3, section4]

        connected_sections = self.connector.connect_sections(sections, section2)  # noqa

        for section in connected_sections:
            assert_that(list(section_connections(section)),
                        has_length(greater_than(0)))
            assert_that(is_connected(section))
