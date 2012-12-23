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
Configuration for pyherc
"""
import random
from pyherc.rules.public import ActionFactory
from pyherc.rules import RulesEngine
from pyherc.rules import Dying
from pyherc.rules.move.factories import MoveFactory
from pyherc.rules.move.factories import WalkFactory
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.attack.factories import MeleeCombatFactory
from pyherc.rules.inventory.factories import InventoryFactory
from pyherc.rules.inventory.factories import PickUpFactory, DropFactory
from pyherc.rules.inventory.equip import EquipFactory
from pyherc.rules.inventory.unequip import UnEquipFactory
from pyherc.generators import ItemGenerator, CreatureGenerator
from pyherc.generators.level.portals import PortalAdderFactory

from pyherc.generators.level.generator import LevelGeneratorFactory
from pyherc.generators.level.config import LevelGeneratorFactoryConfig

from pyherc.generators import EffectsFactory

from pyherc.generators import ItemConfigurations

class Configuration(object):
    """
    Configuration object for Herculeum
    """
    def __init__(self, base_path, model):
        """
        Default constructor

        Args:
            base_path: path to resources directory
            model: Model to register with factories
        """
        super(Configuration, self).__init__()
        self.resolution = None
        self.full_screen = None
        self.caption = None
        self.action_factory = None
        self.base_path = None
        self.item_generator = None
        self.creature_generator = None
        self.player_generator = None
        self.level_generator_factory = None
        self.level_size = None
        self.base_path = base_path
        self.model = model
        self.rng = random.Random()
        self.rules_engine = None

    def initialise(self, context):
        """
        Initialises configuration
        """
        self.level_size = (80, 30)

        self.initialise_generators(context)
        self.initialise_level_generators(context)
        self.initialise_factories(context)

    def initialise_factories(self, context):
        """
        Initialises action factory, sub factories and various generators
        """
        print('Initialising action sub system')

        dying_rules = Dying()

        walk_factory = WalkFactory(self.level_generator_factory)
        move_factory = MoveFactory(walk_factory)

        effect_factory = EffectsFactory()

        configurators = self.get_configurators(context.config_package,
                                               'init_effects')

        for configurator in configurators:
            effects = configurator(context)
            for effect in effects:
                effect_factory.add_effect(effect[0], effect[1])

        unarmed_combat_factory = UnarmedCombatFactory(effect_factory,
                                                      dying_rules)
        melee_combat_factory = MeleeCombatFactory(effect_factory,
                                                  dying_rules)
        attack_factory = AttackFactory([
                                        unarmed_combat_factory,
                                        melee_combat_factory])

        drink_factory = DrinkFactory(effect_factory,
                                     dying_rules)

        inventory_factory = InventoryFactory([PickUpFactory(),
                                             DropFactory(),
                                             EquipFactory(),
                                             UnEquipFactory()])

        self.action_factory = ActionFactory(
                                            self.model,
                                            [move_factory,
                                            attack_factory,
                                            drink_factory,
                                            inventory_factory])

        self.rules_engine = RulesEngine(self.action_factory,
                                        dying_rules)

        print('Action sub system initialised')

    def get_creature_config(self, context):
        """
        Load creature configuration

        :param level_config: namespace of configurations
        :type level_config: Package
        :returns: configuration for creatures
        :rtype: CreatureConfigurations
        """
        config = {}

        configurators = self.get_configurators(context.config_package,
                                               'init_creatures')

        for configurator in configurators:
            creatures = configurator(context)
            for creature in creatures:
                config[creature.name] = creature

        return config

    def get_player_config(self, context):
        """
        Load player configuration

        :param level_config: namespace of configurations
        :type level_config: Package
        :returns: configuration for player characters
        :rtype: CreatureConfigurations

        .. versionadded:: 0.8
        """
        config = {}

        configurators = self.get_configurators(context.config_package,
                                               'init_players')

        for configurator in configurators:
            creatures = configurator(context)
            for creature in creatures:
                config[creature.name] = creature

        return config

    def get_item_config(self, context):
        """
        Load item configuration

        :param level_config: namespace of configurations
        :type level_config: Package
        :returns: configuration for items
        :rtype: ItemConfigurations
        """
        config = ItemConfigurations(self.rng)

        configurators = self.get_configurators(context.config_package,
                                               'init_items')

        for configurator in configurators:
            items = configurator(context)
            for item in items:
                config.add_item(item)

        return config

    def get_configurators(self, location, function_name):
        """
        Get functions to configure given sub-system
        """

        config_modules = map(lambda x: getattr(location, x),
                             filter(lambda x: x[0] != '_',
                                    dir(location)))
        configurators = map(lambda x: getattr(x, function_name),
                            filter(lambda y: hasattr(y, function_name),
                                   config_modules))

        return configurators

    def initialise_generators(self, context):
        """
        Initialise generators
        """
        print('Initialising generators')

        self.item_generator = ItemGenerator(
                                    self.get_item_config(context))

        self.creature_generator = CreatureGenerator(
                                        self.get_creature_config(context),
                                        self.model,
                                        self.item_generator,
                                        self.rng)

        self.player_generator = CreatureGenerator(
                                        self.get_player_config(context),
                                        self.model,
                                        self.item_generator,
                                        self.rng)

        print('Generators initialised')

    def initialise_level_generators(self, context):
        """
        Initialise level generators

        :param level_config: module containing level configurations
        :type level_config: module
        """
        print('Initialising level generators')

        config = LevelGeneratorFactoryConfig([],
                                             [],
                                             [],
                                             [],
                                             [],
                                             [],
                                             self.level_size)

        configurators = self.get_configurators(context.config_package,
                                               'init_level')

        for configurator in configurators:
            self.extend_configuration(config,
                                      configurator(self.rng,
                                                   self.item_generator,
                                                   self.creature_generator,
                                                   self.level_size))

        portal_adder_factory = PortalAdderFactory(
                                config.portal_adder_configurations,
                                self.rng)

        self.level_generator_factory = LevelGeneratorFactory(
                                                    portal_adder_factory,
                                                    config,
                                                    self.rng)

        print('Level generators initialised')

    def extend_configuration(self, config, new_config):
        """
        Sums two configurations together

        Args:
            config: config to extend
            new_config: items to add to configuration
        """
        config.room_generators.extend(new_config.room_generators)
        config.level_partitioners.extend(new_config.level_partitioners)
        config.decorators.extend(new_config.decorators)
        config.item_adders.extend(new_config.item_adders)
        config.creature_adders.extend(new_config.creature_adders)
        config.portal_adder_configurations.extend(
                                    new_config.portal_adder_configurations)


