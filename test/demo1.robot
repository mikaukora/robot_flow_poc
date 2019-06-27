*** Settings ***

Resource            demo1_keywords.robot
Suite Setup         Setup Browser
Suite Teardown      Close All Browsers

*** Variables ***

${COUNTER}=         0

@{SEARCH_TEXTS}=    Qentinel  Flow based programming
@{SEARCH_IMAGES}=   Robotic software testing  Cat  Dog  Porche

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
    ${COUNTER_MAX}=  GetMax  @{SEARCH_TEXTS}

    ${MATCH}=    EqualVal    ${COUNTER}    ${COUNTER_MAX}
    Run Keyword If     ${MATCH}
    ...  Set Suite Variable    ${OUTPUT}    False

    ${COUNTER}=    IncVal    ${COUNTER}
    Set Suite Variable    ${COUNTER}

More images?
    Set Suite Variable  ${OUTPUT}       True
    ${COUNTER_MAX}=  GetMax  @{SEARCH_IMAGES}

    ${MATCH}=    EqualVal    ${COUNTER}    ${COUNTER_MAX}
    Run Keyword If     ${MATCH}
    ...  Set Suite Variable    ${OUTPUT}    False

    ${COUNTER}=    IncVal    ${COUNTER}
    Set Suite Variable    ${COUNTER}

Reset Counters
    Set Suite Variable  ${COUNTER}      0

Start
    Log    Start

End
    Sleep  5
    Log    End


*** keywords ***

GetMax
    [arguments]  @{MyList}
    ${COUNTER_MAX}=  GetLength  ${MyList}
    ${COUNTER_MAX}=  DecVal  ${COUNTER_MAX}
    [return]  ${COUNTER_MAX}
