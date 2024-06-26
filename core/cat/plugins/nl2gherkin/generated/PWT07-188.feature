Feature: Engine Cooling Fan Control
  As a vehicle electronics system, I want to ensure that the cooling fans turn off when the ignition is switched back on and the engine coolant temperature falls below a certain threshold or after a specified time period.

Scenario: Ignition On, Coolant Temperature High, then Switched Off
  Given the ignition status is "on" and the engine is running
  And the head coolant temperature sensor reading is greater than 108 degrees Celsius
  When I set the accessory switch to off and keep the head coolant temperature sensor reading high for 320 seconds
  Then the cooling fan relay low side should be off and the cooling fan relay high speed should be on

Scenario: Ignition Off, Coolant Temperature High, then Switched On
  Given the ignition status is "off"
  And the head coolant temperature sensor reading is greater than 98.5 degrees Celsius
  When I set the ignition status to "on" and keep the head coolant temperature sensor reading high for 320 seconds
  Then the cooling fan relay low side should be off and the cooling fan relay high speed should be on