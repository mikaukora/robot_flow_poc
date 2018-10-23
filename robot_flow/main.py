import click
from robot_flow import get_tests
from robot_flow import list_graph

@click.group()
def cli():
    """Entry point for commands."""
    pass

cli.add_command(get_tests.get_tests)
cli.add_command(list_graph.list_graph)
