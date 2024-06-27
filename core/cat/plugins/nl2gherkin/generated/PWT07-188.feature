Feature: PWT07-246/477 Test Scenario
  Scenario: Ignition On and Off, Head Coolant Temp Sensor Test
    Given VehState.INIgnitionStatus is 5 (Ignition)
    And nEngine is greater than 0
    And no DTC to be logged on ECM

    When Head Coolant Temp Sensor (I_A_CTS1) is set to more than 108 degC
    Then pass criteria 1 is met

    And B_KL15 is set to 0 (Accessory)
    And keep Head Coolant Temp Sensor (I_A_CTS1) at more than 108 degC

    When B_KL15 is set to 1 (Ignition without cranking) after 320 seconds
    Then pass criteria 2 is met

    Given NIgnitionStatus is 0

    When NIgnitionStatus is 5 or TCoolant is less than 98.5 Deg or After Run Timer is 320 seconds
    Then O_S_FAN1 is Off (12V) and O_S_FAN2 is On (0V)
    And O_S_FAN1 is Off (12V) and O_S_FAN2 is Off (12V)

    When rFan1ECM is set to 0%
    Then ECM should not send any Speed request to ZC1 to turn on the HTR fan