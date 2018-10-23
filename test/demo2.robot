*** Settings ***
Resource            keywords.robot
Suite Setup         Setup Tests
Suite Teardown      Close All Browsers

*** Variables ***
${OUTPUT}=          True
${COUNTER}=         0
${COUNTER_MAX}=     2
@{SEARCH_TERMS}     dog   cat    moomin
${SEARCH_TERM}=     None

*** Test Cases ***

Configure search
    [Documentation]         Set search term
    Log    @{SEARCH_TERMS}[${COUNTER}]
    ${VAL}         evaluate   "@{SEARCH_TERMS}[${COUNTER}]"
    Log    ${VAL}
    Log    ${SEARCH_TERM}   console=True
    Set Suite Variable      ${SEARCH_TERM}    ${VAL}

Do search
    [Documentation]         Test basic image search
    Appstate                Google Images
    Typetext                Search                  ${SEARCH_TERM}\n
    VerifyText              ${SEARCH_TERM}
    LogScreenshot

More?
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
