#!/usr/bin/env python
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
Module for herculeum main configuration
"""
import pyherc.config
from herculeum.gui.surfaceManager import SurfaceManager

class Configuration(pyherc.config.Configuration):
    """
    Configuration for herculeum
    """

    def __init__(self, model, config_package, controls):
        """
        Default constructor

        :param model: model to use in configuration
        :param type: Model
        """
        super(Configuration, self).__init__(model)

        self.surface_manager = SurfaceManager()
        self.surface_manager.load_resources()

        self.context = ConfigurationContext(config_package,
                                            self.surface_manager)

        self.controls = controls

    def initialise(self):
        """
        Initialise configuration
        """
        super(Configuration, self).initialise(self.context)

class ConfigurationContext(object):
    """
    Class to relay information between different configuration phases

    .. versionadded:: 0.6
    """
    def __init__(self, config_package, surface_manager):
        """
        Default constructor

        :param config_package: package containing configurations
        :type config_package: Package
        :param surface_manager: manager to handle graphics
        :type surface_manager: SurfaceManager
        """
        super(ConfigurationContext, self).__init__()
        self.config_package = config_package
        self.surface_manager = surface_manager
