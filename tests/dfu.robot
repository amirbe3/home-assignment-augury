
*** Settings ***
Library    OperatingSystem
Library    Process

*** Test Cases ***
DFU Happy Flow
    [Documentation]    Verify endpoint DFU succeeds with valid conditions
    Run Process    python    -c    from augury_api import poll_endpoint_for_dfu, api_post_version_to_dfu_channel; api_post_version_to_dfu_channel("DFU_MOXA-EP1-0001", "ep1_11.swu"); print(poll_endpoint_for_dfu("MOXA-EP1-0001"))    shell=True

DFU Fails Due To Backlog
    [Documentation]    Verify DFU fails when backlog is not empty
    Run Process    python    -c    from augury_api import set_endpoint_backlog, poll_endpoint_for_dfu, api_post_version_to_dfu_channel; set_endpoint_backlog("MOXA-EP1-0001", 1); api_post_version_to_dfu_channel("DFU_MOXA-EP1-0001", "ep1_12.swu"); print(poll_endpoint_for_dfu("MOXA-EP1-0001"))    shell=True

DFU Fails Due To Low Battery
    [Documentation]    Verify DFU fails when battery is below threshold
    Run Process    python    -c    from augury_api import set_endpoint_battery, poll_endpoint_for_dfu, api_post_version_to_dfu_channel; set_endpoint_battery("MOXA-EP1-0001", 2000); api_post_version_to_dfu_channel("DFU_MOXA-EP1-0001", "ep1_13.swu"); print(poll_endpoint_for_dfu("MOXA-EP1-0001"))    shell=True
