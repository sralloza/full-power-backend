import subprocess

import click
import typer

app = typer.Typer(add_completion=False)


def info(msg):
    typer.secho(msg, fg="bright_green")


def warning(msg):
    typer.secho(msg, fg="bright_yellow")


def error(msg):
    typer.secho(msg, fg="bright_red")


def catch_subprocess_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except subprocess.CalledProcessError:
            error("Error using git")
            raise typer.Abort()

    return wrapper


def ensure_clean_dir() -> bool:
    r = subprocess.run(
        ["git", "status", "-s"], check=True, shell=True, capture_output=True
    )
    if r.stdout.decode("utf8"):
        warning("Stashing untracked changes")
        subprocess.run(["git", "stash", "-u"], check=True, shell=True)
        return False
    return True


def unstash_changes():
    info("Unstashing changes")
    subprocess.run(["git", "stash", "pop"], check=True, shell=True)


def fetch_remote():
    info("Fetching remote")
    subprocess.run(["git", "fetch", "-p"], shell=True, check=True)


def checkout_master():
    info("Checking out master")
    subprocess.run(["git", "checkout", "master"], shell=True, check=True)


def merge_origin_master():
    info("Merging master with origin/master")
    subprocess.run(["git", "merge", "origin/master"], shell=True, check=True)


def get_current_branch() -> str:
    info("Getting current branch")
    result = subprocess.run(
        ["git", "branch"], shell=True, check=True, capture_output=True
    )
    text = result.stdout.decode("utf8")
    branches = [x.strip() for x in text.splitlines() if x.startswith("*")]
    if len(branches) > 1:
        raise click.ClickException("Error getting current branch")

    return branches[0].strip("* ")


def remove_feature_branch(old_branch: str):
    info("Removing feature branch [%s]" % old_branch)
    subprocess.run(["git", "branch", "-d", old_branch], shell=True, check=True)


@catch_subprocess_errors
def clean_after_pr():
    stashed = not ensure_clean_dir()
    old_branch = get_current_branch()

    fetch_remote()
    checkout_master()
    merge_origin_master()
    remove_feature_branch(old_branch)

    if stashed:
        unstash_changes()


@app.command()
def main():
    """This script is designed to be executed after creating a Pull Request and merging it in GitHub.

    !!! note
        You must be in the feature branch before using this script.

    This script will:

    1. **Fetch** the last changes to update `origin/master`
    2. **Merge** `master` into `origin/master`
    3. **Remove** feature branch

    """
    clean_after_pr()


if __name__ == "__main__":
    app()
