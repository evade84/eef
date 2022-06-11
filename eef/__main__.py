import typer

from eef.commands import node, pool


def main():
    app = typer.Typer()
    app.add_typer(pool.app, name="pool", help="Do something with pools.")
    app.add_typer(node.app, name="node", help="Information about the current node.")
    app()


if __name__ == "__main__":
    main()
