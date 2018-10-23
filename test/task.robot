*** Settings ***

Suite Setup       Log   In suite setup       console=True
Suite Teardown    Log   In suite teardown    console=True
Test Setup        Log   In test setup        console=True
Test Teardown     Log   In test teardown     console=True

*** Variables ***
${VISITED}=    False

*** Test cases ***

task_a
    Log   In task_a    console=True

task_b
    Log   In task_b    console=True
    Sleep    5

branch_c
    Log   In branch_c    console=True
    Run Keyword If     '${VISITED}' == 'True'    Set Suite Variable    ${OUTPUT}    True
    Run Keyword If     '${VISITED}' == 'False'   Set Suite Variable    ${OUTPUT}    False
    Set Suite Variable    ${VISITED}    True

task_d
    Log   In task_d    console=True

task_e
    Log   In task_e    console=True
    Sleep    5

task_f
    Log   In task_f    console=True
    Sleep    5
