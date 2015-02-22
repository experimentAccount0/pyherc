;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation either version 3 of the License or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not see <http://www.gnu.org/licenses/>.

(defn add-ground-set [gfx base]
  (.add-icon gfx base (+ ":ground/" base ".png") " ")
  (.add-icon gfx (+ base "_1") (+ ":ground/" base "_1.png") " ")
  (.add-icon gfx (+ base "_3") (+ ":ground/" base "_3.png") " ")
  (.add-icon gfx (+ base "_5") (+ ":ground/" base "_5.png") " ")
  (.add-icon gfx (+ base "_7") (+ ":ground/" base "_7.png") " ")
  (.add-icon gfx (+ base "_13") (+ ":ground/" base "_13.png") " ")
  (.add-icon gfx (+ base "_15") (+ ":ground/" base "_15.png") " ")
  (.add-icon gfx (+ base "_17") (+ ":ground/" base "_17.png") " ")
  (.add-icon gfx (+ base "_35") (+ ":ground/" base "_35.png") " ")
  (.add-icon gfx (+ base "_37") (+ ":ground/" base "_37.png") " ")
  (.add-icon gfx (+ base "_57") (+ ":ground/" base "_57.png") " ")
  (.add-icon gfx (+ base "_135") (+ ":ground/" base "_135.png") " ")
  (.add-icon gfx (+ base "_137") (+ ":ground/" base "_137.png") " ")
  (.add-icon gfx (+ base "_157") (+ ":ground/" base "_157.png") " ")
  (.add-icon gfx (+ base "_357") (+ ":ground/" base "_357.png") " ")
  (.add-icon gfx (+ base "_1357") (+ ":ground/" base "_1357.png") " ")
)

(defn init-graphics [context]
  "load graphcis"
  (let [[gfx context.surface-manager]]
    (add-ground-set gfx "ground_rock1")
    (add-ground-set gfx "ground_rock2")
    (add-ground-set gfx "ground_rock3")
    (add-ground-set gfx "ground_rock4")
    (add-ground-set gfx "ground_soil1")
    (add-ground-set gfx "ground_soil2")
    (add-ground-set gfx "ground_soil3")
    (add-ground-set gfx "ground_soil4")
    (add-ground-set gfx "ground_tile3")
    (add-ground-set gfx "ground_tile4")
    (add-ground-set gfx "ground_wood4")))
