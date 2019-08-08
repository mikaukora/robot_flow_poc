#
#  Copyright 2019     Qentinel
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import click
from robot.parsing.model import TestData


@click.command()
@click.argument('filename')
def get_tests(filename):
    """Returns tests found in Robot FW script."""
    suite = TestData(parent=None, source=filename)
    for testcase in suite.testcase_table:
        print(testcase.name)
