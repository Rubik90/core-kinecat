Here is the Gherkin scenario:

Feature: Ignition State Transition
Scenario:
Given the vehicle is in Ignition State 2
And an Authorised key is present inside or outside the vehicle
And the door is open
And the LV Battery State of Charge is not 'Pre-UVP'
And the Ethernet Status and ADI are stable and communicating
When the above conditions are met
Then the Ignition State shall transition to State 3