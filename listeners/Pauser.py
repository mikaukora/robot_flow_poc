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

import time


class Pauser(object):
    """ This is simple listener for Robot Framework,
        adding given delay in seconds (default 3 seconds)
        to each test step.

        Usage:
        robot --listener Pauser:5 test/
    """
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, delay=3):
        self.delay = int(delay)

    def start_keyword(self, data, result):
        time.sleep(self.delay)
