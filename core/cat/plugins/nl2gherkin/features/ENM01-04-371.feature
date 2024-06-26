Feature: ENM01-04-371
Once the EDSU is in 'Charge Starting' state AND charge exit conditions are not met [380], the EDSU shall transition to 'Charging' state if EDSU confirms charging is in progress from positive charging current.
The EDSU shall stay in 'Charge Starting' state for a minimum calibratable time period before transition to 'Charging' state if charge exit conditions are not met [380].
Appropriate debounce and filtering mechanism shall apply to SoC increase and positive charging current confirmation.

  Scenario Outline: ENM01-04-371_1
    Given HybridStatus is Standby
    When HybridStatus is set to ChrgStarting for a <calibratable> time period
    And minSOC_BMS increasing
    And NIPUOBCStatus is Normal
    Then NHybridStatus is HybridOBC
    Examples: 
      | calibratable |
      | 1            |
      | 2            |

  Scenario Outline: ENM01-04-371_2
    Given HybridStatus is Standby
    When HybridStatus is set to ChrgStarting for a <calibratable> time period
    And IOBCHV > <HSU_Cal>
    And NIPUOBCStatus is Normal
    Then NHybridStatus is HybridOBC
    Examples: 
      | calibratable | HSU_Cal |
      | 1            | 1       |
      | 2            | 2       |

  Scenario Outline: ENM01-04-371_3
    Given HybridStatus is Standby
    When HybridStatus is set to ChrgStarting for a <calibratable> time period
    And minSOC_BMS increasing
    And NIPUOBCStatus is Derate
    Then NHybridStatus is HybridOBC
    Examples: 
      | calibratable |
      | 1            |
      | 2            |

  Scenario Outline: ENM01-04-371_4
    Given HybridStatus is Standby
    When HybridStatus is set to ChrgStarting for a <calibratable> time period
    And IOBCHV > <HSU_Cal>
    And NIPUOBCStatus is Derate
    Then NHybridStatus is HybridOBC
    Examples: 
      | calibratable | HSU_Cal |
      | 1            | 1       |
      | 2            | 2       |