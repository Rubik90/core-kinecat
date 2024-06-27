Feature: ZC1 ASW Transition to RUN Mode
  Scenario: ZC1 transitions back in RUN mode if up reasons become active in POST-RUN
    Given NEcuUpReasonZc1 is not equal to 0
    When the unit is in POST-RUN and tShutdownZc1TimeoutThresh has been exceeded
    And NNetworkManagerStatusZc1 is not equal to NWK_MGR_STANDBY
    Then ZC1 status should be RUN
    And a DTC should be raised