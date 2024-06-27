Feature: PreCondition Testing
  Scenario: Module Goes to Standby
    Given Ethernet.NIgnitionStatus = 0x1
    When ZC1_XCP.NPwtCoolingNetworkRequest = 1
    Then Network communication is stopped on all networks and the module goes to standby