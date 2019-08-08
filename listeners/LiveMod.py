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

import copy


class LiveMod(object):
    """
    This is an example listener using just start_suite and end_suite
    to modify executed cases dynamically.

    Usage:
    robot --listener listeners\LiveMod.py test\demo1.robot
    """

    ROBOT_LISTENER_API_VERSION = 3
    MOD = 0

    def str2test(self, testname, tests):
        """ Return test case object based on testname. """
        for t in tests:
            if testname == t.name:
                return t
        return None

    def start_suite(self, data, result):
        print("Running suite: {}".format(data))
        print("Available tests: {}".format(data.tests._items))

        # Copy available tests and clear the actual execution list
        self.orig_tests = copy.deepcopy(data.tests)
        data.tests.clear()

        # Append some case to execution list
        test_case = self.str2test('Start', self.orig_tests)
        data.tests.append(test_case)

    def start_test(self, data, result):
        print("Running test: {}".format(data))
        print("Available tests: {}".format(data.parent.tests._items))

    def end_test(self, data, result):
        print("Ending test: {}".format(data))

        # Append some case to execution list. This is just an example of
        # flow control for testing purposes.
        if self.MOD == 0:
            test_case = self.str2test('Start', self.orig_tests)
            data.parent.tests.append(test_case)
            self.MOD = 1
        elif self.MOD == 1:
            test_case = self.str2test('End', self.orig_tests)
            data.parent.tests.append(test_case)
            self.MOD = 2

        print("Available tests: {}".format(data.parent.tests._items))
