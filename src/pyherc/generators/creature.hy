;; -*- coding: utf-8 -*-

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

(require hy.contrib.anaphoric)
(import [pyherc.aspects [log_debug log_info]])
(import [pyherc.data [Character]])
(import [pyherc.data.effects [EffectHandle]])
(import [functools [partial]])

(defn generate-creature [configuration model item-generator rng name]
  "Generate creature"
  (let [[config (get configuration name)]
	[creature (Character model)]
	[item-adder (partial add-item creature rng item-generator)]]
    (setv creature.name (:name config))
    (setv creature.body (:body config))
    (setv creature.finesse (:finesse config))
    (setv creature.mind (:mind config))
    (setv creature.hit_points (:hp config))
    (setv creature.max_hp (:hp config))
    (setv creature.speed (:speed config))
    (setv creature.icon (:icons config))
    (setv creature.attack (:attack config))
    (map (fn [handle] (.add-effect creature (EffectHandle handle.trigger
							  handle.effect
							  handle.parameters
							  handle.charges))) 
	 (:effect-handles config))
    (ap-each (:effects config) (.add-effect creature (.clone it)))
    ;;(map (fn [effect] (.add-effect creature (.clone effect))) (:effects config))
    (ap-each (:inventory config) (item-adder it))

    (when (:ai config)
      (setv creature.artificial-intelligence ((:ai config) creature)))
    creature))

(defn creature-config [name body finesse mind hp speed icons attack 
		       &optional [ai nil] [effect-handles nil] [effects nil]
		       [inventory nil] [description nil]]
  "Create configuration for a creature"
  {:name name :body body :finesse finesse :mind mind :hp hp :speed speed
   :icons icons :attack attack :ai ai :description description
   :effect-handles (if effect-handles effect-handles [])
   :effects (if effects effects [])
   :inventory (if inventory inventory [])})

(defn add-item [creature rng item-generator item-spec]
  (let [[item-count (.randint rng (:min-amount item-spec) (:max-amount item-spec))]]
    (for [item (range item-count)]
      (.append creature.inventory
	       (.generate-item item-generator (:item-name item-spec))))))

(defn inventory-config [item-name min-amount max-amount probability]
  "Create configuration for inventory item"
  {:item-name item-name :min-amount min-amount :max-amount max-amount
   :probability probability})
