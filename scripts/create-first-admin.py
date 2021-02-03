import logging

logging.basicConfig(level=logging.INFO)

import typer
from sqlalchemy.orm.session import Session

from app import crud
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.user import UserCreateAdmin

logger = logging.getLogger(__name__)

app = typer.Typer(add_completion=False)


def create_user(db: Session, *, username: str = None, password: str = None):
    username = username or settings.first_superuser
    password = password or settings.first_superuser_password

    user = crud.user.get_by_username(db, username=username)
    if user:
        typer.secho("User %r was already created" % username, fg="bright_red")
        return

    user_in = UserCreateAdmin(username=username, password=password, is_admin=True)
    user = crud.user.create(db, obj_in=user_in)

    db.commit()
    typer.secho("User created", fg="bright_green")


@app.command()
def main(
    username: str = typer.Option(
        settings.first_superuser,
        help="username of the admin",
        show_default="[settings.first_superuser](../settings.md#database)",  # type: ignore
    ),
    password: str = typer.Option(
        settings.first_superuser_password,
        help="password of the admin",
        show_default="[settings.first_superuser_password](../settings.md#database)",  # type: ignore
    ),
):
    """Creates an admin. If not provided, username and password are taken from settings."""
    typer.secho("Starting create-first-admin script")

    db = SessionLocal()
    create_user(db, username=username, password=password)

    typer.secho("create-first-admin script ended")


if __name__ == "__main__":
    app()
