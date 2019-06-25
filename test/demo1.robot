*** Settings ***
Resource            demo1_keywords.robot
*** Settings ***
Suite Setup         Setup Browser
Suite Teardown      Close All Browsers

*** Variables ***
${OUTPUT}=          True
${COUNTER}=         0
#${COUNTER_MAX}=     2

@{SEARCH_TEXTS}=    Qentinel  Robocorptech
@{CURRENT_TERM}=    None

@{SEARCH_IMAGES}=   Robotic software testing  Cat  Dog

*** Test Cases ***

Get Search Term
    Set Suite Variable    ${CURRENT_TERM}    ${SEARCH_TEXTS[${COUNTER}]}

Get Search Image
    Set Suite Variable    ${CURRENT_TERM}    ${SEARCH_IMAGES[${COUNTER}]}

Search Text
    [Documentation]         Test basic title search
    Appstate                Google
    Typetext                Search                  ${CURRENT_TERM}
    ClickText               Google Search
    VerifyText              ${CURRENT_TERM}

Search Image
    [Documentation]         Test basic image search
    Appstate                Google Images
    Typetext                Search                  ${CURRENT_TERM}\n
    LogScreenshot
    VerifyText              ${CURRENT_TERM}

More items?
    Set Suite Variable  ${OUTPUT}       True
    Log    Checking counter
    Log    ${COUNTER}    console=True
    ${COUNTER_MAX}=  GetLength  ${SEARCH_TEXTS}
    ${COUNTER_MAX}=  DecVal  ${COUNTER_MAX}
    Log  ${COUNTER_MAX}  console=True
    ${MATCH}=    EqualVal    ${COUNTER}    ${COUNTER_MAX}
    Run Keyword If     ${MATCH}    Set Suite Variable    ${OUTPUT}    False
    ${COUNTER}=    IncVal    ${COUNTER}
    Set Suite Variable    ${COUNTER}

More images?
    Set Suite Variable  ${OUTPUT}       True
    Log    Checking counter
    Log    ${COUNTER}    console=True
    ${COUNTER_MAX}=  GetLength  ${SEARCH_IMAGES}
    ${COUNTER_MAX}=  DecVal  ${COUNTER_MAX}
    Log  ${COUNTER_MAX}  console=True
    ${MATCH}=    EqualVal    ${COUNTER}    ${COUNTER_MAX}
    Run Keyword If     ${MATCH}    Set Suite Variable    ${OUTPUT}    False
    ${COUNTER}=    IncVal    ${COUNTER}
    Set Suite Variable    ${COUNTER}

Reset Counters
    Set Suite Variable  ${COUNTER}      0
    #Set Suite Variable  ${COUNTER_MAX}  2

Start
    Log    Start

End
    Sleep  5
    Log    End
