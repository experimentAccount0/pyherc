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
Module for spell factory
"""
from pyherc.aspects import logged

from pyherc.data.magic import Spell

class SpellGenerator():
    """
    Factory for creating spells
    
    .. versionadded:: 0.9
    """
    @logged
    def __init__(self):
        """
        Default constructor
        """
        pass
    
    @logged
    def create_spell(self, spell_name, target):
        """
        Create a spell
        
        :param spell_name: name of the spell
        :type spell_name: string
        :param target: target of the spell
        :type target: Character
        :returns: ready to use spell
        :rtype: Spell
        """
        new_spell = Spell()
        new_spell.target.append(target)

        return new_spell