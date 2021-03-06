;; -*- coding: utf-8 -*-

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

(defmulti generate-artefact [artefact-type &optional [seed None]]
  "select method based on artefact-type parameter"
  artefact-type)

(default-method generate-artefact [artefact-type &optional [seed None]]
  "create blueprint of specific type and instantiate it"
  (-> (create-blueprint artefact-type seed)
      (instantiate-blueprints)))

;; create blueprint for an artefact or part of it
(defmulti create-blueprint [artefact-type &optional [seed None]]
  "select method based on artefact-type parameter"
  artefact-type)

(default-method create-blueprint [artefact-type &optional [seed None]]
  "no definition was found for artefact, throw an error"
  (assert False "no artefact blueprint defined"))

;; create instance of an artefact based on one or more blueprint
(defmulti instantiate-blueprints [&rest blueprints]
  "select method based on type in blueprint"
  (if (= (len blueprints) 1)
    (:type (first blueprints))
    (tuple (list-comp (:type blueprint) [blueprint blueprints]))))

(default-method instantiate-blueprints [&rest blueprints]
  "no definition found, thrown an error"
  (assert False "no instantiator found for blueprint"))

;; modify blueprint to contain elements of another
(defmulti modify-blueprint [modifier-type blueprint]
  "modify blueprint"
  modifier-type)

(default-method modify-blueprint [modifier-type blueprint]
  "no definition was found, throw an error"
  (assert False "no blueprint defined"))

(defn blueprint-types [blueprint]
  "types of this blueprint"
  (:blueprints blueprint))

(defn add-blueprint-type [blueprint type]
  "add new subtype"
  (when (not (in :blueprints blueprint))
    (assoc blueprint :blueprints []))
  (.append (:blueprints blueprint) type))
