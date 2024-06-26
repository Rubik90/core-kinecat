Here is the Gherkin scenario:

Feature: Vehicle System Test 01-01-460 - Ignition Status and Door Status
  As a vehicle system tester, 
  I want to test that the IgnSt2Timeout Timer resets when either of the doors are opened or closed while in Transport Mode
  So that the timer is properly reset

Scenario: Reset IgnSt2Timeout Timer on Door Open or Close
  Given NIgnitionStatus is set to 2
  And NDoorLOpenStatus and/or NDoorROpenStatus have changed value
  When NIgnitionStatus equals 2 and NDoorLOpenStatus has changed value or NDoorROpenStatus has changed value
  Then the IgnSt2Timeout Timer shall be reset