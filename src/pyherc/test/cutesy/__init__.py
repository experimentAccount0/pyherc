# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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

# flake8: noqa

"""
Package for testing dsl
"""

from .characters import Goblin, Adventurer, Wizard
from .characters import strong, weak
from .weapons import Dagger, Sword, Club, Bow, Arrows, Warhammer
from .armours import LeatherArmour, ScaleMail, PlateMail
from .items import Rune
from .dictionary import at_
from .dictionary import affect, with_, potent_poison, weak_poison
from .dictionary import carrying
from .dictionary import place, middle_of, right_of, Level
from .dictionary import make, drop, hit, wait_, gain_domain_
from .dictionary import has_dropped, has_less_hit_points
from .dictionary import cast_spell
from .dictionary import take_random_step
