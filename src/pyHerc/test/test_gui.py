#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

import pyHerc.gui.windows

class test_gameWindow:

    def test_formattingEventHistory_LessThanFiveItems(self):
        window = pyHerc.gui.windows.GameWindow(None, None)
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        result = window.formatEventHistory()
        assert(result[0] == 'one')
        assert(result[1] == 'two')

    def test_formattingEventHistory_FiveItems(self):
        window = pyHerc.gui.windows.GameWindow(None, None)
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        window.eventHistory.append('three')
        window.eventHistory.append('four')
        window.eventHistory.append('five')
        result = window.formatEventHistory()
        assert(result[0] == 'one')
        assert(result[1] == 'two')
        assert(result[2] == 'three')
        assert(result[3] == 'four')
        assert(result[4] == 'five')

    def test_formattingEventHistory_MoreThanFiveItems(self):
        window = pyHerc.gui.windows.GameWindow(None, None)
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        window.eventHistory.append('three')
        window.eventHistory.append('four')
        window.eventHistory.append('five')
        window.eventHistory.append('six')
        result = window.formatEventHistory()
        print result
        assert(len(result) == 5)
        assert(result[0] == 'two')
        assert(result[1] == 'three')
        assert(result[2] == 'four')
        assert(result[3] == 'five')
        assert(result[4] == 'six')