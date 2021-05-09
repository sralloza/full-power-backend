import traceback

import typer
from sqlalchemy_utils import create_database, database_exists

from app.db.session import engine

app = typer.Typer(add_completion=False)


def ensure_database() -> None:
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
    except:
        tb = traceback.format_exc()
        typer.secho(f"Error executing query:\n\n{tb}", fg="bright_red")
        raise typer.Abort()


@app.command()
def main():
    """Creates the database if it doesn't exist (valid for mysql servers)."""
    ensure_database()


if __name__ == "__main__":
    app()
