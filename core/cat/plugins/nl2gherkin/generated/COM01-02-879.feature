Feature: Diagnostic Window Activation for MCU
  Scenario: Diagnostic Window Enabled when Conditions Met
    Given NNetworksResponseValidZc1(bit3) is true
    And Quick response time has elapsed
    And NFaultUnlatchRequestMCU is equal to 0x0 latch
    And neMotorROutboard is received
    When Hybrid_CAN Network status is active
    And EDSU Fault Unlatching Mechanism is not requested
    Then Diag Window MCU is Enabled