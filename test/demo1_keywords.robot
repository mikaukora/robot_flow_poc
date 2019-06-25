*** Settings ***
Library             Dialogs
Library             QWeb
Library             String
Library             demo_lib.py


*** Variables ***
${BROWSER}                  ff

*** Keywords ***
Setup Browser
    Open Browser    about:blank    ${BROWSER}

End suite
    Close All Browsers

Appstate
    [Documentation]     AppState handler
    [Arguments]         ${state}
    ${state}=           Convert To Lowercase    ${state}

    Run Keyword If     '${state}' == 'qentinel'
    ...                 Qentinel

    Run Keyword If     '${state}' == 'google'
    ...                 Google

    Run Keyword If     '${state}' == 'google images'
    ...                 Google Images

    Run Keyword If     '${state}' == 'yliopisto'
    ...                 Yliopisto

Qentinel
    Go To           https://qentinel.com/en

Google
    Go To           http://www.google.com/intl/en/

Google Images
    Go To           http://images.google.com/intl/en/

