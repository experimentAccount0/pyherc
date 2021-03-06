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

(require [pyherc.aspects [*]])
(import [pyherc.aspects [log-debug log-info]]
        [pyherc.rules.mitosis.action [MitosisAction]]
        [pyherc.rules.factory [SubActionFactory]])

(defclass MitosisFactory [SubActionFactory]
  [--init-- (fn [self character-generator rng character-limit]
              "default constructor"
              (-> (super) (.--init--))
              (setv self.character-generator character-generator)
              (setv self.rng rng)
              (setv self.character-limit character-limit)
              (setv self.action-type "mitosis"))
   can-handle (fn [self parameters]
                "can this factory handle a given action"
                (= self.action-type parameters.action-type))
   get-action (fn [self parameters]
                "create mitosis action"
                (MitosisAction parameters.character
                               self.character-generator
                               self.rng
                               self.character-limit))])
