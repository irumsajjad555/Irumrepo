*** Settings ***
Library    Autosphere.Browser

*** Keywords ***
Keep Open
    Open Browser    https://www.amazon.com
*** Tasks ***
Testing
    Keep Open