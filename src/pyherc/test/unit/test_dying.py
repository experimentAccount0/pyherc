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
Tests for dying
"""
from pyherc.rules import Dying, ActionFactory, InventoryParameters
from pyherc.test.builders import CharacterBuilder, ItemBuilder
from pyherc.test.matchers import DropActionParameterMatcher
from mockito import mock, verify, any, when

class TestDying(object):
    """
    Tests for dying
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestDying, self).__init__()

    def test_wielded_weapons_are_dropped_when_dying(self):
        """
        Test that wielded weapons are dropped when dying
        """
        action_factory = mock(ActionFactory)
        when(action_factory).get_action(any()).thenReturn(mock())

        item = ItemBuilder().build()

        character = (CharacterBuilder()
                        .with_hit_points(-1)
                        .with_item(item)
                        .build())

        dying = Dying(action_factory)

        dying.check_dying(character)

        verify(action_factory).get_action(DropActionParameterMatcher(item))
