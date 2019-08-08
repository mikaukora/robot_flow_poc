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

class Modifier(object):
    """ Usage:
        robot_flow get_tests.py test/test.robot > tests.txt
        (modify test list file)
        robot --listener Modifier:"tests.txt" test/
    """
    
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, filename):
        print("Got filename: {}".format(filename))
        self.filename = filename
        self.tests = self.parse_tests(self.filename)
        
    def parse_tests(self, filename):
        with open(filename) as f:
            tests = f.readlines()
        print("Read {}".format(tests))
        return [t.strip() for t in tests]

    def start_suite(self, data, result):
        if data.tests:
            print("Original: {}".format(data.tests))
            print("Replacing with: {}".format(self.tests))

            modified = []
            # Find object from existing tests in a script and
            # move to a new list if still needed. It could be moved
            # to another location, removed or duplicated.
            for testname in self.tests:
                for old in data.tests:
                    if testname == old.name:
                        print("found")
                        modified.append(old)

            data.tests = modified
            print("Now using: {}".format(data.tests))

    def start_test(self, data, result):
        data.keywords.create(name='Log', args=['Keyword added by listener'])
        print("Keywords: {}".format(data.keywords))
            
    def end_test(self, data, result):
        print("Test ended")
