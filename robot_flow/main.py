import click
from robot_flow import get_tests

@click.group()
def cli():
    """Entry point for commands."""
    pass

cli.add_command(get_tests.get_tests)
