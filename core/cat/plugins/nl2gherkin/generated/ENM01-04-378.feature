Feature: Precondition
  As a driver, I want the EDSU to enter 'Charge Complete' and disable OBC when the HV Battery is full and the vehicle is in ignition or accessory mode.

Scenario: Preconditions are met
  Given the NIgnitionStatus is either "Accessory" or "Ignition"
  And the chargeState_BMS is "CHARGESTATE_COMPLETE"
  When the EDSU enters the 'Charge Complete' state
  Then the NHybridStatus should be "Charge Complete"
  And the NIPUCommand should not be "OBC Disabled"

Scenario: Preconditions are not met
  Given the NIgnitionStatus is neither "Accessory" nor "Ignition"
  Or the chargeState_BMS is not "CHARGESTATE_COMPLETE"
  When the EDSU enters the 'Charge Complete' state
  Then an error should occur

Note: The above Gherkin scenarios are based on the input provided and do not include any additional information.