Feature: Precondition Procedure
  Scenario: Driver starts vehicle with full HV battery
    Given Ethernet.NHybridFault != 3 "Level 2 Fault" && Ethernet.NignitionStatus = 3 || 5
    When HV.NIpuVehicletethered = 2 "Tethered_communicated"
    And Hybrid.minSOC_BMS increasing
    And Hybrid.chargeState_BMS == 1 "CHARGESTATE_COMPLETE"
    Then Hybrid.minSOC_BMS ≥ ZC1_XCP.rEdsuHvSocUpperLimitP for t > ZC1_XCP.tEdsuHvChargeCompleteThP
    And Ethernet.NHybridStatus = 3 "CNTCT_clsd_HV_ready_TrqNotAv" || 4 "CNTCT_closed_HV_ready_TrqAv"
    When Ethernet.NHybridStatus = 8 "ChrgStarting" for ZC1_XCP.tEdsuChargeStartThP
    And Ethernet.NHybridStatus = 9 "HybridOBC"
    And Ethernet.NIPUCommand != 1 "OBC Disabled"
    Then Ethernet.NHybridStatus = 0xA "Charge Complete"