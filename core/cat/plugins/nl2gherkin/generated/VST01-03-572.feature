Here is the generated Gherkin scenario:

Feature: PreCondition HLTR Pump LIN Request

Scenario: Activate HLTR Cooling Network Request
Given Ethernet.NIgnitionStatus is 0x1
When ZC1_XCP.NPwtCoolingNetworkRequest is 1 and NPwtCoolingNetworkRequest is equal to 0x1
Then NEcuUpReason[HLTRCooling_bit] should be set to 1