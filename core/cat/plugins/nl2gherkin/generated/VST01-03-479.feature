Here is the generated Gherkin scenario:

Feature: ZC1 ASW Transition to RUN Mode
  As a network manager, I want the ZC1 ASW to transition to RUN mode when an up reason becomes active in POST-RUN state.
  
  Scenario: ZC1 transitions to RUN mode due to up reason activation
    Given the unit is in POST-RUN state and tShutdownZc1TimeoutThresh has been exceeded
    And NNetworkManagerStatusZc1 is not NWK_MGR_STANDBY
    When NEcuUpReasonZc1 becomes active
    Then ZC1 status should be RUN