*** Settings ***
Resource            keywords.robot
Suite Setup         Setup Tests
Suite Teardown      Close All Browsers

*** Variables ***
${OUTPUT}=          True
${COUNTER}=         0
${COUNTER_MAX}=     1

*** Test Cases ***

Basic search
    [Documentation]         Test basic title search
    Appstate                Google
    Typetext                Search                  Qentinel
    ClickText               Google Search
    VerifyText              Bertel Jungin aukio 7

Image search
    [Documentation]         Test basic image search
    Appstate                Google Images
    Typetext                Search                  Qentinel\n
    LogScreenshot
    VerifyText              Robotic Software Testing

Repeat?
    Log    Checking counter
    Log    ${COUNTER}    console=True
    ${MATCH}=    EqualVal    ${COUNTER}    ${COUNTER_MAX}
    Run Keyword If     ${MATCH}    Set Suite Variable    ${OUTPUT}    False
    ${COUNTER}=    IncVal    ${COUNTER}
    Set Suite Variable    ${COUNTER}

Start
    Log    Start

End
    Log    End
