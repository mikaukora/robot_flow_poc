import click
from robot.parsing.model import TestData

@click.command()
@click.argument('filename')
def get_tests(filename):
    """Returns tests found in Robot FW script."""
    suite = TestData(parent=None, source=filename)
    for testcase in suite.testcase_table:
        print(testcase.name)
