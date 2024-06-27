Feature: Ignition State Transition
  Scenario: Ignition State 2 to State 3 Triggered
    Given the ignition state is 2
    And the door is open (inside or outside)
    And the battery state of charge is not "Pre-UVP"
    And the Ethernet status and ADI are stable and communicating
    When an authorized key is detected inside or outside the vehicle
    Then the ignition state should transition to 3