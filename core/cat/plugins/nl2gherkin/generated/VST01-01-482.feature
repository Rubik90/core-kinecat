Feature: Ignition Status and Door Status Test
  Scenario: Reset IgnSt2Timeout Timer for door open or close while ignition status is 2
    Given NIgnitionStatus = 2
    When NDoorLOpenStatus changes value || NDoorROpenStatus changes value
    Then Reset IgnSt2Timeout Timer