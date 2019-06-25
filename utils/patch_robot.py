#!/usr/bin/env python

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
