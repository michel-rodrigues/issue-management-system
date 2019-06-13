Feature: Issue reporting

  Scenario: reporting a new issue
      Given an empty issue log
      When we report a new issue
      Then it should have created a new issue
      Then it should have recorded the issuer
      Then it should have recorded the description
