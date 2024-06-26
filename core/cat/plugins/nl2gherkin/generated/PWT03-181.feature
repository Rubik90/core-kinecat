Feature: Engine Overboost Limitation
  As an engineer, I want to ensure that the engine air charge is limited when an overboost condition occurs.

Scenario: Engine Air Charge Limited During Overboost
  Given the engine is running (Ignition 5) and brakes are pressed
  And there is an overboost condition (pBoost > 2.5 Bar)
  Then the calculated load shall be less than or equal to 80% for the remainder of the ignition cycle