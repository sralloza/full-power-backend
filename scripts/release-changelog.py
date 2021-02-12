import subprocess
from datetime import datetime
from pathlib import Path

import typer

app = typer.Typer(add_completion=False)


class ChangelogEditor:
    def __init__(self):
        self.lines = Path("CHANGELOG.md").read_text("utf8").splitlines()
        self.current_release = self.find_current_version()

    def release(self, new_version):
        self.fix_links(new_version)
        self.fix_header(new_version)

    def fix_header(self, new_version):
        for i, line in enumerate(self.lines):
            if "[Unreleased]" in line and "##" in line:
                today_str = datetime.now().strftime("%Y-%m-%d")
                self.lines.insert(i + 1, f"## [{new_version}] - {today_str}")
                self.lines.insert(i + 1, "")
                return

    def fix_links(self, new_version):
        for i, line in enumerate(self.lines):
            if "[unreleased]" in line and "#" not in line:
                self.lines[i] = line.replace(self.current_release, new_version)
                new_link = "https://github.com/BelinguoAG/full-power-backend/compare/v{}...v{}".format(
                    self.current_release, new_version
                )
                new_link = f"[{new_version}]: {new_link}"
                self.lines.insert(i + 1, new_link)
                return

    def find_current_version(self):
        for line in self.lines:
            if "[unreleased]" in line and "#" not in line:
                return line.split("/")[-1].split("...")[0][1:]
        raise Exception

    def write(self):
        Path("CHANGELOG.md").write_text("\n".join(self.lines) + "\n", "utf8")


def catch_subprocess_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except subprocess.CalledProcessError:
            typer.secho("Error using git", fg="bright_red")
            raise typer.Abort()

    return wrapper


@catch_subprocess_errors
def create_commit():
    r = subprocess.run(["git", "status"], check=True, shell=True, capture_output=True)
    if "no changes added to commit" not in r.stdout.decode("utf8"):
        typer.secho(
            "There are staged files, can't create changelog commit",
            fg="bright_red",
        )
        raise typer.Abort()
    subprocess.run(["git", "add", "CHANGELOG.md"], check=True, shell=True)
    subprocess.run(
        ["git", "commit", "-m", "docs: release new version in changelog"],
        check=True,
        shell=True,
    )


@catch_subprocess_errors
def add_tag(tag: str):
    subprocess.run(["git", "tag", "-a", f"v{tag}", "-m", ""], check=True, shell=True)
    subprocess.run(["git", "push", "origin", f"v{tag}"], check=True, shell=True)


@app.command()
def release(
    new_version: str,
    commit: bool = typer.Option(
        True, " /--no-commit", " /--nc", help="Commits the result"
    ),
    tag: bool = typer.Option(True, " /--nt", help="Create tag"),
    offline: bool = typer.Option(False, "--offline", help="Disables commit and tag"),
):
    """Releases a new version in the changelog.

    Notes:

    * Use `--no-commit` or `--nc` to disable the autocommit.
    * Use `--nt` to disable the tag creation.

    If the autocommit is disabled, the autotag will be disabled too, regardless of the `offline` option.
    """

    if offline:
        tag = commit = False

    if not commit:
        tag = False

    changelog = ChangelogEditor()
    changelog.release(new_version)
    changelog.write()

    if commit:
        create_commit()

    if tag:
        add_tag(new_version)


if __name__ == "__main__":
    app()
