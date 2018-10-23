# Robot Framework tools

## Install

`pip install -e .`

## Running robot_flow

`robot_flow --help`

`robot_flow get-tests --help`

## Listeners

Listeners are defined in [listeners](./listeners/) directory.

#### Add pause between keywords

To slow down operation, delay (s) between executed keywords can be defined:

`robot --listener Pauser:5 test/`

#### Modify test case list

Get available tests:

`robot_flow get-tests test/test.robot > tests.txt`

(modify test list file by changing order, duplicating items, removing items)

Run updated test case list:

`robot --listener Modifier:"tests.txt" test/`
