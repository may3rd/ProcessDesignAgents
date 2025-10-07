import click
from processdesignagents.graph.design_graph import build_graph

@click.command()
@click.argument("problem")
def design(problem):
    graph = build_graph()
    result = graph.invoke({"problem_statement": problem})
    click.echo(result)

if __name__ == "__main__":
    design()