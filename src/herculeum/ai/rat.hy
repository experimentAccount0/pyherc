;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

(require [pyherc.macros [*]])
(require [pyherc.fsm [*]])

(import [random]
        [herculeum.ai.movement [home-location select-home wallside?
                                travel-home whole-level arrived-destination?
                                map-home-area home-area fill-along-walls
                                clear-current-destination patrol-home-area
                                close-in along-walls]]
        [herculeum.ai.combat [select-current-enemy current-enemy closest-enemy
                              melee detected-enemies]]
        [pyherc.data.geometry [in-area area-4-around]]
        [pyherc.data.constants [Duration]]
        [pyherc.ai [a-star :as a* show-alert-icon show-confusion-icon]]
        pyherc)


(defstatemachine RatAI []
  "AI routine for rats"
  (--init-- [character] (state character character))

  "find a place to call a home"
  (finding-home initial-state
                (on-activate (when (not (home-location character))
                               (select-home character wallside?)))
                (active (travel-home (a* (whole-level)) character))
                (transitions [(arrived-destination? character) patrolling]
                             [(detected-enemies character) fighting]))
  
  "patrol alongside the walls"
  (patrolling (on-activate (when (not (home-area character))
                             (map-home-area character
                                            (fill-along-walls (. character level)))) 
                           (clear-current-destination character))
              (active (one-of (patrol-home-area (a* (along-walls)) character)
                              (call wait character Duration.fast)))
              (transitions [(detected-enemies character) fighting]))
  
  "fight enemy"
  (fighting (on-activate (clear-current-destination character)
                         (select-current-enemy character closest-enemy)
                         (show-alert-icon character (current-enemy character)))
            (active (if (in-area area-4-around (. character location) 
                                 (. (current-enemy character) location))
                      (melee character (current-enemy character))
                      (close-in (a* (whole-level)) 
                                character 
                                (. (current-enemy character) location))))
            (on-deactivate (show-confusion-icon character))
            (transitions [(not (detected-enemies character)) finding-home])))
