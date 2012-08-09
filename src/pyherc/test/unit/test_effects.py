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
Module for testing effects
"""

#pylint: disable=W0614
from pyherc.rules.effects import Heal
from pyherc.rules.effects import Poison
from pyherc.rules.effects import Effect
from pyherc.rules.effects import EffectsFactory
from pyherc.rules.effects import EffectHandle
from pyherc.rules.public import ActionFactory
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.events import PoisonAddedEvent, Event
from random import Random
from pyherc.test.builders import CharacterBuilder, ItemBuilder
from pyherc.test.builders import EffectHandleBuilder, ActionFactoryBuilder
from pyherc.test.builders import EffectBuilder
from pyherc.test.builders import LevelBuilder
from pyherc.test.matchers import has_effect, has_effects, has_no_effects

from mockito import mock, when, any, verify
from hamcrest import * #pylint: disable=W0401

class TestEffects(object):
    """
    Tests for effects in general
    """

    def test_effect_triggered_while_drinking(self):
        """
        Test that effect will be triggered when drinking potion
        """
        effect_factory = mock(EffectsFactory)
        effect_spec = mock(EffectHandle)
        effect = mock (Effect)
        effect.duration = 0
        potion = mock()

        effect_spec.charges = 2
        when(potion).get_effect_handles('on drink').thenReturn([effect_spec])
        when(effect_factory).create_effect(any(),
                                           target = any()).thenReturn(effect)

        model = mock()
        action_factory = ActionFactory(model = model,
                                       factories = [DrinkFactory(effect_factory)])

        character = (CharacterBuilder()
                        .with_model(model)
                        .build())
        character.drink(potion,
                        action_factory)

        verify(effect).trigger()

    def test_effect__triggered_when_hitting_target(self):
        """
        Test that effect is triggered when attack hits target
        """
        effect = mock()
        effect.duration = 0
        model = mock()
        rng = mock()

        when(rng).randint(1, 6).thenReturn(1)

        effect_factory = mock(EffectsFactory)
        when(effect_factory).create_effect(any(),
                                           target = any()).thenReturn(effect)

        action_factory = (ActionFactoryBuilder()
                            .with_model(model)
                            .with_attack_factory()
                            .with_effect_factory(effect_factory)
                            .build())

        attacker = (CharacterBuilder()
                        .with_effect_handle(
                                EffectHandleBuilder()
                                    .with_trigger('on attack hit'))
                        .with_location((5, 5))
                        .build())

        defender = (CharacterBuilder()
                        .with_location((6, 5))
                        .build())

        level = (LevelBuilder()
                    .with_character(attacker)
                    .with_character(defender)
                    .build())

        attacker.perform_attack(3,
                                action_factory,
                                rng)

        verify(effect).trigger()

    def test_creating_effect(self):
        """
        Test that effect can be created and triggered immediately
        """
        effect_factory = EffectsFactory()
        effect_factory.add_effect(
                            'major heal',
                            {'type': Heal,
                            'duration': 0,
                            'frequency': 0,
                            'tick': 0,
                            'healing': 10})

        potion = (ItemBuilder()
                        .with_effect(
                            EffectHandleBuilder()
                                .with_trigger('on drink')
                                .with_effect('major heal')
                                .with_charges(2))
                        .build())

        action_factory = ActionFactory(model = mock(),
                                       factories = [DrinkFactory(effect_factory)])

        character = (CharacterBuilder()
                        .with_hit_points(1)
                        .with_max_hp(10)
                        .build())

        character.drink(potion,
                        action_factory)

        assert_that(character.hit_points, is_(equal_to(10)))
        assert_that(character, has_no_effects())

    def test_timed_effect_is_triggered(self):
        """
        Test that timed effect is triggered only after enough time
        has passed
        """
        effect_factory = EffectsFactory()
        effect_factory.add_effect(
                            'major heal',
                            {'type': Heal,
                            'duration': 12,
                            'frequency': 3,
                            'tick': 3,
                            'healing': 10})

        potion = (ItemBuilder()
                        .with_effect(
                            EffectHandleBuilder()
                                .with_trigger('on drink')
                                .with_effect('major heal')
                                .with_charges(2))
                        .build())

        action_factory = ActionFactory(model = mock(),
                                       factories = [DrinkFactory(effect_factory)])

        character = (CharacterBuilder()
                        .with_hit_points(1)
                        .with_max_hp(10)
                        .build())

        character.drink(potion,
                        action_factory)

        assert_that(character, has_effects(1))

    def test_effect_expiration_event_is_raised(self):
        """
        Test that effect expiration raises an event
        """
        model = mock()

        character = (CharacterBuilder()
                        .with_effect(EffectBuilder()
                                        .with_duration(0)
                                        .with_tick(10)
                                        .with_frequency(10))
                        .with_model(model)
                        .build())

        character.remove_expired_effects()

        verify(model, times = 2).raise_event(any(Event))

class TestEffectsInMelee(object):
    """
    Test of effect creation and handling in melee
    """

    def __init__(self):
        """
        Default constructor
        """
        super(TestEffectsInMelee, self).__init__()

        self.attacker = None
        self.defender = None
        self.model = None
        self.action_factory = None

    def setup(self):
        """
        Setup test case
        """
        self.model = mock()

        effect_factory = EffectsFactory()
        effect_factory.add_effect(
                            'poison',
                            {'type': Poison,
                            'duration': 12,
                            'frequency': 3,
                            'tick': 3,
                            'damage': 5})

        self.action_factory = (ActionFactoryBuilder()
                                    .with_attack_factory()
                                    .with_effect_factory(effect_factory)
                                    .build())

        self.attacker = (CharacterBuilder()
                            .with_location((5, 5))
                            .with_effect_handle(EffectHandleBuilder()
                                                 .with_trigger('on attack hit')
                                                 .with_effect('poison'))
                            .with_model(self.model)
                            .build())

        self.defender = (CharacterBuilder()
                            .with_location((5, 4))
                            .with_hit_points(50)
                            .with_model(self.model)
                            .build())

        level = (LevelBuilder()
                    .with_character(self.attacker)
                    .with_character(self.defender)
                    .build())

    def test_add_effect_in_melee(self):
        """
        Test that effect can be added as a result of unarmed combat
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        self.attacker.perform_attack(1,
                                     self.action_factory,
                                     rng)

        assert_that(self.defender, has_effect())

    def test_effects_do_not_stack(self):
        """
        Test that single type of effect will not added twice
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        self.attacker.perform_attack(1,
                                     self.action_factory,
                                     rng)
        self.attacker.perform_attack(1,
                                     self.action_factory,
                                     rng)

        assert_that(self.defender, has_effects(1))

    def test_effect_creation_event_is_raised(self):
        """
        Test that event is raised to indicate an effect was created
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        self.attacker.perform_attack(1,
                                     self.action_factory,
                                     rng)

        verify(self.model).raise_event(any(PoisonAddedEvent))
