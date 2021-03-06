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

(setv __doc__ "helper macros AIs")

(defmacro third [collection]
  `(get ~collection 2))

(defmacro fourth [collection]
  `(get ~collection 3))

(defmacro very-rarely [code else-code]
  `(do (import random)
       (if (< (.randint random 1 100) 10) ~code
	   ~else-code)))

(defmacro rarely [code else-code]
  `(do (import random)
       (if (< (.randint random 1 100) 25) ~code
           ~else-code)))

(defmacro sometimes [code else-code]
  `(do (import random)
       (if (< (.randint random 1 100) 50) ~code
           ~else-code)))

(defmacro often [code else-code]
  `(do (import random)
       (if (< (.randint random 1 100) 75) ~code
           ~else-code)))

