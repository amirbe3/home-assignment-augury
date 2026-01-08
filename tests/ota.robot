*** Settings ***
Library    OperatingSystem
Library    Process

*** Test Cases ***
OTA Update Happy Flow
    [Documentation]    Verify that node OTA update succeeds with valid firmware
    Run Process    python    src/demo.py    shell=True
