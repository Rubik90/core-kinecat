Here is the Gherkin scenario:

Feature: EDSU Charging State Transition
  As a charging system, I want the EDSU to transition to the correct state based on certain conditions.

Scenario: Transition from 'Charge Starting' to 'Charging'
  Given the EDSU is in 'Charge Starting' state
  And charge exit conditions are not met [380]
  And the EDSU confirms charging is in progress from positive charging current
  When the time period for transition has elapsed
  Then the EDSU shall be in 'Charging' state

Scenario: Stay in 'Charge Starting' until conditions met
  Given the EDSU is in 'Charge Starting' state
  And charge exit conditions are not met [380]
  And the minimum calibratable time period for transition has elapsed
  When the charge exit conditions are met [380]
  Then the EDSU shall be in 'Charging' state