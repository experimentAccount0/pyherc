;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(import [pyherc.aspects [log_debug]]
        [random])
(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)

(defn new-tile []
  "create a tile with default values"
  {:floor nil
   :wall nil
   :ornamentations []
   :trap nil
   :location_types []
   :items []
   :creatures []
   :portal nil})

(defn get-tile [level location]
  "get tile at given location"
  (when (in location level.tiles)
    (get level.tiles location)))

(defn get-or-create-tile [level location]
  "get tile at given location"
  (when (not (in location level.tiles))
    (assoc level.tiles location (new-tile)))
  (get level.tiles location))

(defn floor-tile [level location &optional tile-id]
  "get/set floor tile at given location"
  (if tile-id
    (do (let [[map-tile (get-or-create-tile level location)]]
          (assoc map-tile :floor tile-id)
          (:floor map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:floor map-tile))))))

(defn wall-tile [level location &optional tile-id]
  "get/set wall tile at given location"
  (if tile-id
    (do (let [[map-tile (get-or-create-tile level location)]]
          (assoc map-tile :wall tile-id)
          (:wall map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:wall map-tile))))))

#d(defn add-portal [level location portal &optional other-end]
    "add a new portal"
    (setv portal.level level)
    (setv portal.location location)
    (floor-tile level location portal.icon)
    (assoc (get-tile level location) :portal portal)
    (when other-end
      (.set-other-end portal other-end)
      (.set-other-end other-end portal)))

#d(defn get-portal [level location]
    "get portal at given location"
    (:portal (get-tile level location)))

#d(defn level-size [level]
    "get size of level (x₀, x₁, y₀, y₁)"
    (let [[x₀ 0] [x₁ 0] [y₀ 0] [y₁ 0]]
      (ap-each level.tiles
               (do
                (when (< (first it) x₀) (setv x₀ (first it)))
                (when (> (first it) x₁) (setv x₁ (first it)))
                (when (< (second it) y₀) (setv y₀ (second it)))
                (when (> (second it) y₁) (setv y₁ (second it)))))
      #t(x₀ x₁ y₀ y₁)))

#d(defn find-free-space [level]
    "find a free location within level"
    (let [[free-tiles (list-comp (first pair)
                                 [pair (.items level.tiles)] 
                                 (:floor (second pair)))]]
      (.choice random free-tiles)))

#d(defn blocks-movement [level location]
    "check if given location blocks movement"
    (let [[map-tile (get-tile level location)]]
      (if map-tile
        (:wall map-tile)
        true)))