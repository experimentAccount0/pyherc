Feature: Armours
  as an character
  in order to protect myself
  I want to use different kinds of armours

  Background:
     Given Pete is Adventurer
       And Uglak is Goblin
       And Pete is standing next to Uglak

  @automated
  Scenario: Damage reduction
      Given Pete wields club
        And Uglak wears leather armour
       When Pete hits Uglak
       Then damage should be reduced

  @automated
  Scenario: Well protected
      Given Uglak wields dagger
        And Pete wears scale mail
       When Uglak hits Pete
       Then damage should be 1

  @automated
  Scenario: Completely protected
      Given Uglak wields dagger
        And Pete wears plate mail
       When Uglak hits Pete
       Then damage should be 0

  @automated
  Scenario: Moving in heavy armour is slow
      Given Pete wears scale mail
       When Pete takes a step
       Then Pete should move slower than without scale mail
