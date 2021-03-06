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

(require [archimedes [*]])
(require [hymn.dsl [*]])

(import [hamcrest [assert-that is- equal-to has-item is-not :as is-not-
                   not-none greater-than greater_than_or_equal_to]]
        [hypothesis.strategies [integers]]
        [hymn.types.either [->either either]]
        [herculeum.society.data [new-society raw-resources society-name
                                 new-project project-name projects start-project
                                 buildings new-building building-name
                                 add-building new-person person-name
                                 project-duration
                                 depleted very-low low medium high very-high 
                                 overflowing]]
        [herculeum.society.rules [process-projects-m process-raw-resources-m
                                  advance-time-m]]
        [herculeum.society.generators [instantiate-blueprints]]
        [pyherc.generators.artefact [create-blueprint modify-blueprint]]
        [herculeum.test.matchers.society [has-building? 
                                          has-resources?
                                          has-more-resources-than?
                                          has-less-resources-than?
                                          blueprint-for]])

(fact "depleted is less than medium"
      (assert-that (< depleted medium)
                   (is- (equal-to True))))

(fact "very-high is greater than very-low"
      (assert-that (> very-high very-low)
                   (is- (equal-to True))))

(background high-society
            society (new-society "high society")
            chief (new-person "Chief Atticus")
            project (new-project "housing construction"
                                 :building (new-building "housing"))
            long-project (new-project "monolith" :duration 10))

(background mining-society
            society (new-society "mining society")
            mine (new-building "mine"
                               :produces 1)
            giant-mine (new-building "giant mine"
                                     :produces 20)
            _ (add-building society mine))

(background poor-society
            society (new-society "poor society")
            _ (raw-resources society depleted)
            project (new-project "statue"))

(fact "society can have a name"
      (with-background high-society [society]
        (assert-that (society-name society)
                     (is- (equal-to "high society")))
        (society-name society "low society")
        (assert-that (society-name society)
                     (is- (equal-to "low society")))))

(fact "raw resources of society can be manipulated"
      (with-background high-society [society]
        (raw-resources society low)
        (assert-that (raw-resources society)
                     (is- (equal-to low)))))

(fact "project can have a name"
      (with-background high-society [project]
        (assert-that (project-name project)
                     (is- (equal-to "housing construction")))
        (project-name project "pool construction")
        (assert-that (project-name project)
                     (is- (equal-to "pool construction")))))

(fact "project can be started"
      (with-background high-society [society project]
        (start-project society project)
        (assert-that (projects society) 
                     (has-item project))))

(fact "project has duration"
      (with-background high-society [project]
        (assert-that (project-duration project)
                     (is- (equal-to 1)))
        (project-duration project 5)
        (assert-that (project-duration project)
                     (is- (equal-to 5)))))

(fact "processing projects decreases their duration"
      (with-background high-society [society long-project]
        (start-project society long-project)
        (assert-right (do-monad [status (process-projects-m society)]
                                status)
                      (assert-that (project-duration long-project)
                                   (is- (equal-to 9))))))

(fact "completed projects are removed for queue"
      (with-background high-society [society project]
        (start-project society project)
        (assert-right (do-monad [status (process-projects-m society)]
                                status)
                      (assert-that (projects society)
                                   (is-not- (has-item project))))))

(fact "completed project adds a new building"
      (with-background high-society [society project]
        (start-project society project)
        (assert-right (do-monad [status (process-projects-m society)]
                                status)
                      (assert-that (buildings society)
                                   (has-building? "housing")))))

(fact "building has a name"
      (let [building (new-building "small house")]
        (assert-that (building-name building)
                     (is- (equal-to "small house")))
        (building-name building "large house")
        (assert-that (building-name building)
                     (is- (equal-to "large house")))))

(fact "special buildings produce raw resources"
      (with-background mining-society [society mine]
        (let [old-resources (raw-resources society)]
          (assert-right (do-monad [status (process-raw-resources-m society)]
                                  status)
                        (assert-that society 
                                     (has-more-resources-than? old-resources))))))

(fact "society can never have more than overflowing amount of resources"
      (with-background mining-society [society giant-mine]
        (let [old-resources (raw-resources society)]
          (add-building society giant-mine)
          (assert-right (do-monad [status (advance-time-m society)]
                                  status)
                        (assert-that society
                                     (is-not- (has-more-resources-than? overflowing)))))))

(fact "processing projects consume resources"
      (with-background high-society [society project] 
        (start-project society project)
        (let [old-resources (raw-resources society)]
          (assert-right (do-monad [status (advance-time-m society)]
                                  status)
                        (assert-that society
                                     (has-less-resources-than? old-resources))))))

(fact "society can never have less than depleted amount of resources"
      (with-background poor-society [society project]
        (start-project society project)
        (assert-right (do-monad [status (advance-time-m society)]
                                status)
                      (assert-that society
                                   (has-resources? depleted)))))

(fact "person has name"
      (with-background high-society [chief]
        (assert-that (person-name chief)
                     (is- (equal-to "Chief Atticus")))
        (person-name chief "Chief Africanus")
        (assert-that (person-name chief)
                     (is- (equal-to "Chief Africanus")))))

(fact "smith blueprint is marked as smith"
      (assert-that (->> (create-blueprint 'human)
                        (modify-blueprint 'smith))
                   (is- (blueprint-for 'smith))))

(fact "blueprint modifiers can be chained"
      (variants :seed (integers :min-value 1))
      (assert-that (:mind (->> (create-blueprint 'human seed)
                               (modify-blueprint 'wise)
                               (modify-blueprint 'scribe)))
                   (is- (greater_than_or_equal_to 7))))

(fact "human blueprint saves seed for future use"
      (assert-that (:seed (create-blueprint 'human 5))
                   (is- (equal-to 5))))
