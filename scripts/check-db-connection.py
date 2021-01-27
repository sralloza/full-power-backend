import traceback

import typer

from app.db.session import SessionLocal

app = typer.Typer(add_completion=False)


def init() -> None:
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
    except:
        tb = traceback.format_exc()
        typer.secho(f"Error connecting to database:\n\n{tb}", fg="bright_red")
        raise typer.Abort()


@app.command()
def main():
    """Checks the connection to the database."""
    typer.echo("Setting up connection to database...")
    init()
    typer.secho("Connection success", fg="bright_green")


if __name__ == "__main__":
    app()
