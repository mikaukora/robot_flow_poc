# Robot Framework tools

## Install

`pip install -e .`

## Running robot_flow

Help is available for sub-commands

`robot_flow --help`

`robot_flow get-tests --help`

Get tests/tasks from Robot FW file.

`robot_flow get-tests test.robot`

Get tests/tasks from GRAPHML file, with optional verbosity:

`robot_flow list-graph task.graphml -v`

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
