;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2013 Tuukka Turto
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

(setv __doc__ "module for AI routines for rats")

(import [pyherc.aspects [logged]]
	[pyherc.ai.pathfinding [a-star]]
	[random]
	[math [sqrt]])

(require pyherc.ai.helpers)

(defmacro diagonal-wall [info]
  (quasiquote (get (unquote info) 0)))

(defmacro adjacent-wall [info]
  (quasiquote (get (unquote info) 1)))

(defmacro empty-corridor [info]
  (quasiquote (get (unquote info) 2)))

(defmacro wall-direction [info]
  (quasiquote (get (unquote info) 3)))

(defclass RatAI []
  [[__doc__ "AI routine for rats"]
   [character None]
   [mode [:find-wall :north]]
   [--init-- (fn [self character]
	       "default constructor"
	       (.--init-- (super RatAI self))
	       (setv self.character character) None)]
   [act (fn [self model action-factory rng] 
	  "check the situation and act accordingly"
	  (rat-act self model action-factory))]])

(with-decorator logged 
  (defn rat-act [ai model action-factory]
    "main routine for rat AI"
    (let [[enemy (enemy-close? ai)]]
      (if enemy (start-fighting ai enemy)))
    (let [[func (get mode-bindings (first ai.mode))]]
      (func ai action-factory))))

(with-decorator logged
  (defn find-wall [ai action-factory]
    "routine to make character to find a wall"
    (let [[wall-info (next-to-wall? ai)]]
      (if wall-info (do (start-following-wall ai wall-info)
			(follow-wall ai action-factory))
	  (if (can-walk? ai action-factory)
	    (walk ai action-factory)
	    (sometimes (walk-random-direction ai action-factory)
		       (wait ai)))))))

(with-decorator logged
  (defn follow-wall [ai action-factory]
    "routine to make character to follow a wall"
    (often (if (can-walk? ai action-factory)
	     (walk ai action-factory)
	     (let [[wall-info (next-to-wall? ai)]]
	       (if wall-info (do (start-following-wall ai wall-info)
				 (wait ai))
		   (walk-random-direction ai action-factory))))
	   (wait ai))))

(with-decorator logged
  (defn fight [ai action-factory]
    "routine to make character to fight"
    (let [[own-location ai.character.location]
	  [enemy (second ai.mode)]
	  [enemy-location enemy.location]
	  [distance (distance-between own-location enemy-location)]]
      (if (< distance 2)
	(attack ai enemy action-factory (.Random random))
	(close-in ai enemy action-factory)))))

(defn attack [ai enemy action-factory rng]
  "attack an enemy"
  (let [[attacker ai.character]
	[attacker-location attacker.location]
	[target-location enemy.location]	
	[attack-direction (map-direction (find-direction attacker-location 
							 target-location))]]
    (.perform-attack attacker attack-direction action-factory rng)))

(defn find-direction [start destination]
  "calculate direction from start to destination"
  (let [[start-x (first start)]
	[start-y (second start)]
	[end-x (first destination)]
	[end-y (second destination)]]
    (if (= start-x end-x)
      (if (< start-y end-y) :south :north)
      (if (= start-y end-y)
	(if (< start-x end-x) :east :west)
	(if (< start-y end-y)
	  (if (< start-x end-x) :south-east :south-west)
	  (if (< start-x end-x) :north-east :north-west))))))

(defn close-in [ai enemy action-factory]
  "get closer to enemy"
  (let [[start-location ai.character.location]
	[end-location enemy.location]
	[(, path connections uptated) (a-star start-location
					      end-location
					      ai.character.level)]]
    (walk ai action-factory (find-direction start-location (second path)))))

(defn enemy-close? [ai]
  "check if there is an enemy close by, returns preferred enemy"
  (let [[level ai.character.level]
	[player ai.character.model.player]]
    (if (< (distance-between player.location ai.character.location) 4) 
      player)))

(defn distance-between [start end]
  "calculate distance between two locations"
  (let [[dist-x (- (first start) (first end))]
	[dist-y (- (second start) (second end))]]
    (sqrt (+ (pow dist-x 2)
          (pow dist-y 2)))))

(defn start-fighting [ai enemy]
  "pick start fighting again enemy"
  (setv ai.mode [:fight
		enemy]))

(defn start-following-wall [ai wall-info]
  (setv ai.mode [:follow-wall 
		 (get-random-wall-direction wall-info)]))

(defn walk-random-direction [ai action-factory]
  "take a random step without changing mode"
  (let [[legal-directions (list-comp direction 
				     [direction (range 1 9)] 
				     (.is-move-legal ai.character
						     (map-direction direction)
						     "walk"
						     action-factory))]]
    (if (len legal-directions) (assoc ai.mode 1
				      (map-direction (.choice random 
							      legal-directions)))
	(assoc ai.mode 1 (map-direction (.randint random 1 8))))
    (if (can-walk? ai action-factory) (walk ai action-factory)
	(wait ai))))

(defn can-walk? [ai action-factory]
  "check if character can walk to given direction"
  (.is-move-legal ai.character
		  (map-direction (second ai.mode))
		  "walk"
		  action-factory))

(defn walk [ai action-factory &optional direction]
  "take a step to direction the ai is currently moving"
  (if direction
    (.move ai.character (map-direction direction) action-factory)
    (.move ai.character (map-direction (second ai.mode)) action-factory)))

(defn wait [ai]
  "make character to wait a little bit"
  (setv ai.character.tick 5))

;; wall-mapping
;; first two elements are offsets for required walls
;; third element is offset for required empty space
;; fourth element is resulting direction
(def wall-mapping [[[-1 1]  [0 1]  [-1 0] :west]
		   [[-1 -1] [0 -1] [-1 0] :west]
		   [[1 1]   [0 1]  [1 0]  :east]
		   [[1 -1]  [0 -1] [1 0]  :east]
		   [[-1 1]  [-1 0] [0 1]  :south]
		   [[1 1]   [1 0]  [0 1]  :south]
		   [[-1 -1] [-1 0] [0 -1] :north]
		   [[1 -1]  [1 0]  [0 -1] :north]])

(defn next-to-wall? [ai]
  "check if ai is standing next to a wall"
  (let [[character ai.character]
	[possible-directions (list-comp (check-wall-mapping character x) 
					[x wall-mapping])]
	[directions (list-comp direction [direction possible-directions] 
			       (not (= direction None)))]]
    (if (> (len directions) 0) {:wall-direction directions} None)))

(defn check-wall-mapping [character wall-mapping]
  "build a list of directions where a wall leads from given location"
  (let [[level character.level]
	[point-1 (map-coordinates character (diagonal-wall wall-mapping))]
	[point-2 (map-coordinates character (adjacent-wall wall-mapping))]
	[point-3 (map-coordinates character (empty-corridor wall-mapping))]]
    (if (and (.blocks-movement level (first point-1) (second point-1))
             (.blocks-movement level (first point-2) (second point-2))
	     (not (.blocks-movement level (first point-3) (second point-3))))
      (wall-direction wall-mapping))))

(defn map-coordinates [character offset]
  "calculate new coordinates from character and offset"
  (let [[character-x (first character.location)]
	[character-y (second character.location)]
	[offset-x (first offset)]
	[offset-y (second offset)]]
    (, (+ character-x offset-x) (+ character-y offset-y))))

(defn get-random-wall-direction [wall-info]
  "select a random direction from the given wall-info"
  (.choice random (:wall-direction wall-info)))

(def direction-mapping {1 :north 2 :north-east 3 :east 4 :south-east 5 :south
			6 :south-west 7 :west 8 :north-west 9 :enter
			:north 1 :north-east 2 :east 3 :south-east 4 :south 5
			:south-west 6 :west 7 :north-west 8 :enter 9})

(defn map-direction [direction]
  "map between keyword and integer directions"
  (get direction-mapping direction))

(def mode-bindings {:find-wall find-wall
		    :follow-wall follow-wall
		    :fight fight})


