# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
Module for testing drop action factory
"""
from hamcrest import assert_that, equal_to, greater_than, is_, is_in, is_not
from mockito import any, mock, verify
from pyherc.data import Model
from pyherc.rules import drop_item
from pyherc.rules.inventory.factories import DropFactory
from pyherc.rules.inventory.interface import InventoryParameters
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  ItemBuilder, LevelBuilder)
from pyherc.test.matchers import event_type_of


class TestDropFactory():
    """
    Tests for drop action factory
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_can_handle_parameters(self):
        """
        Test that drop factory can handle parameter class
        """
        parameters = InventoryParameters(character=mock(),
                                         item=mock(),
                                         sub_action='drop')
        factory = DropFactory()

        can_handle = factory.can_handle(parameters)

        assert_that(can_handle, is_(equal_to(True)))


class TestDropAction():
    """
    Tests for dropping item
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.item = None
        self.level = None
        self.character = None
        self.action_factory = None
        self.model = None

    def setup(self):
        """
        Setup test case
        """
        self.model = mock(Model)
        self.level = LevelBuilder().build()
        self.item = ItemBuilder().build()

        self.character = (CharacterBuilder()
                          .with_item(self.item)
                          .with_level(self.level)
                          .with_location((5, 5))
                          .with_model(self.model)
                          .build())

        self.action_factory = (ActionFactoryBuilder()
                               .with_inventory_factory()
                               .build())

    def test_dropped_item_is_removed_from_inventory(self):
        """
        Test that dropped item is removed from inventory
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        assert_that(self.item,
                    is_not(is_in(self.character.inventory)))

    def test_dropped_item_is_added_on_level(self):
        """
        Test that dropped item ends up on level
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        assert_that(self.item.level,
                    is_(equal_to(self.level)))

    def test_dropped_item_added_to_correct_location(self):
        """
        Test that dropped item is added to correct location
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        assert_that(self.item.location,
                    is_(equal_to(self.character.location)))

    def test_dropping_takes_time(self):
        """
        Dropping an item should move characters time forward
        """
        old_time = self.character.tick

        drop_item(self.character,
                  self.item,
                  self.action_factory)
        new_time = self.character.tick

        assert_that(new_time, is_(greater_than(old_time)))

    def test_dropping_raises_event(self):
        """
        Dropping an item should raise an event
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        verify(self.model).raise_event(event_type_of('drop'))
