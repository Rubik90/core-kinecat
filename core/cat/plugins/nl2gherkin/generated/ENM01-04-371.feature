Feature: EDSU Charging State Transition
  Scenario: Transition from 'Charge Starting' to 'Charging'
    Given NHybridStatus is "ChrgStarting" for a calibratable time period
    And minSOC_BMS is increasing or IOBCHV > Threshold(HSU_Cal)
    And NIPUOBCStatus is either "Normal" or "Derate"
    When the EDSU confirms charging is in progress from positive charging current
    Then NHybridStatus should be set to "HybridOBC"
    And stay in 'Charge Starting' state for a minimum calibratable time period