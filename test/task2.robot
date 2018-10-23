*** Settings ***
Resource            ../resources/keywords.robot
Suite Setup         Setup QVision
Suite Teardown      End suite
Test Setup        Log   In test setup        console=True
Test Teardown     Log   In test teardown     console=True

*** Variables ***
${VISITED}=    False

*** Test cases ***

start
    Log    start               console=True
    Sleep    1

stop
    Log    stop                console=True

calculate_salary
    Log    calculate_salary    console=True
    Sleep    1

create_summary
    Log    create_summary      console=True
    Sleep    1

line_available?
    Log    line_available?     console=True
    Run Keyword If     '${VISITED}' == 'True'    Set Suite Variable    ${OUTPUT}    False
    Run Keyword If     '${VISITED}' == 'False'   Set Suite Variable    ${OUTPUT}    True
    Set Suite Variable    ${VISITED}    True
    Sleep    1

read_line
    Log    read_line           console=True
    Sleep    1

store_to_disk
    Log    store_to_disk       console=True
    Sleep    1

wait_for_file
    Log    wait_for_file       console=True
    Sleep  5

Insert table and delete table
    [Tags]            QExcel
    Appstate          Excel
    #filling some test data
    TypeCell          A1             100
    TypeCell          A2             200
    TypeCell          A3             300
    TypeCell          A4             400
    TypeCell          A5             500
    sleep             2s
    ClickText         Insert         Draw
    VerifyText        PivotTable
    ClickText         Table
    sleep             2s
    ClickIcon         OKCommon       tolerance=0.7
    VerifyText        Column1
    RightClick        Column1        Properties
    HoverOverText     Delete
    ClickText         Delete
    ClickText         Delete Rows
    ClickIcon         3x3cells

Type and read text in cell
    [Tags]            ok
    Appstate          Excel
    TypeCell          A1             teksti
    ${luettu} =       ReadCell     A1
    TypeCell          A3             ${luettu}
