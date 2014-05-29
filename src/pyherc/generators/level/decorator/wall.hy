;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(import [pyherc.generators.level.decorator.basic [Decorator DecoratorConfig]])

(defclass SurroundingDecorator [Decorator]
  [[--init-- (fn [self configuration]
               "default constructor"
               (-> (super) (.--init-- configuration))
               (setv self.wall-tile configuration.wall-tile))]
   [decorate-level (fn [self level]
                     "decorate a level")]])

(defclass SurroundingDecoratorConfig [DecoratorConfig]
  [[--init-- (fn [self level_types wall_tile]
               "default constructor"
               (-> (super) (.--init-- level_types))
               (setv self.wall-tile wall-tile))]])
