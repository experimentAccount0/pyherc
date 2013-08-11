#!/usr/bin/env python3
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
Package for customer pyHamcrest matchers used in testing
"""

from .map_connectivity import is_fully_accessible_via
from .map_connectivity import located_in_room
from .contains_creature import has_creature, is_in, is_not_in
from .active_effects import has_effects, has_no_effects
from .active_effects import has_effect
from .items import does_have_item, does_not_have_item, has_damage
from .effect_collection import has_effect_handle, has_effect_handles
from .event_listener import has_event_listener
from .event import has_marked_for_redrawing
from .character import is_dead
from .inventory_parameters import DropActionParameterMatcher
from .event_parameters import EventType
from .path_finding import continuous_path
from .inventory import is_wearing, does_have
from .attack_parameters import AttackActionParameterMatcher
from .targeting import wall_target_at, void_target
