Feature: Engine Overboost Limitation Test
  Scenario: Verify Overboost Condition and Load Calculation
    Given Ignition is set to 5
    And the engine is running
    And the brake is pressed
    When the overboost condition is generated (pBoost > 2.5Bar)
    Then PID04_CalculatedLoad should be less than or equal to 80% for the remainder of the ignition cycle