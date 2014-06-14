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

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [pyherc.data [distance-between]]
        [pyherc.generators.level.partitioners [section-width section-height
                                               section-floor add-room-connection
                                               section-connections
                                               match-section-to-room
                                               section-floor]]
        [pyherc.generators.level.room.corridor [CorridorGenerator]])

(defn new-room-generator [&rest creators]
  "create a room generator"
  (fn [section]
    (ap-each creators (it section))))

(defn circular-shape [floor-tile]
  "create a circular shape"
  (fn [section]
    (let [[center-x (// (section-width section) 2)]
          [center-y (// (section-height section) 2)]
          [center-point #t(center-x center-y)]
          [radius (min [(- center-x 2) (- center-y 2)])]]
      (for [x_loc (range (section-width section))]
        (for [y_loc (range (section-height section))]
          (when (<= (distance-between #t(x_loc y_loc) center-point) radius)
            (section-floor section #t(x_loc y_loc) floor-tile "room"))))
      (assoc section :center-point center-point)
      (add-room-connection section #t(center-x (- center-y radius)) "up")
      (add-room-connection section #t(center-x (+ center-y radius)) "down")
      (add-room-connection section #t((- center-x radius) center-y) "left")
      (add-room-connection section #t((+ center-x radius) center-y) "right"))))

(defn corridors [floor-tile]
  "create corridors"
    (fn [section]
      "carve corridors"
      (ap-each (section-connections section)
               (let [[room-connection (match-section-to-room section it)]
                     [corridor (CorridorGenerator room-connection
                                                  (.translate-to-section it)
                                                  nil
                                                  floor-tile)]]
                 (.generate corridor)))))

(defn cache-creator [cache-tile item-selector character-selector]
  "create cache creator"
  (fn [section]
    "fill cache with items and characters"
    (section-floor section (:center-point section) cache-tile)))

(defn tomes-and-potions-cache [item-generator]
  "create cache content creator"
  (fn []
    []))

(defn no-characters-cache [character-generator]
  "create cache character creator"
  (fn []
    []))

(defn demo [floor-tile corridor-tile cache-tile item-generator character-generator] 
  (new-room-generator (circular-shape floor-tile)
                      (corridors corridor-tile)
                      (cache-creator cache-tile
                                     (tomes-and-potions-cache item-generator)
                                     (no-characters-cache character-generator))))

