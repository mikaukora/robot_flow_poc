#!/usr/bin/env python
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

""" Replace Robot FW runner.py with given version. """

import os
import pathlib
import shutil
import sys

from robot import running


def verify_file(filename):
    file_found = os.path.isfile(filename)
    if not file_found:
        print(f"Error: File not found: {filename}")
        return False
    return True

if len(sys.argv) != 2:
    print("Usage: patch_robot.py my_runner.py")
    sys.exit(1)

if sys.argv[1].lower() in ["-h", "--help"]:
    print("Usage: patch_robot.py my_runner.py")
    sys.exit(1)

# Check new runner file

new_runner = sys.argv[1]

if not verify_file(new_runner):
    sys.exit(1)

# Check existing Robot FW runner

runner_dir = running.__path__[0]
runner_file = pathlib.Path(runner_dir) / "runner.py"

if not verify_file(runner_file):
    sys.exit(1)

# Overwrite file

proceed = input(f"Overwrite {runner_file} with {new_runner}? y/N ")
if proceed.lower() in ["y", "yes"]:
    try:
        shutil.copyfile(new_runner, runner_file)
    except PermissionError:
        print("Insufficient permissions, consider running in admin mode or use virtual environment")
