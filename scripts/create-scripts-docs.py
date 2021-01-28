import subprocess
import re
from pathlib import Path

import typer

app = typer.Typer(add_completion=False)


def check_script_name(script_name: str):
    if not Path(__file__).with_name(script_name + ".py").is_file():
        raise typer.BadParameter(f"Script 'scripts/{script_name}.py doesn't exist")
    return script_name


@app.command()
def main(
    script_name: str = typer.Argument(
        None, help="Name of the script without extension", callback=check_script_name
    )
):
    """Updates the docs for a script."""

    script_path = f"scripts/{script_name}.py"
    args = ["typer", script_path, "utils", "docs", "--name", script_name]

    r = subprocess.run(args, capture_output=True)
    original_md = r.stdout.decode("utf8").replace("\r\n", "\n").strip() + "\n"
    parsed_md = re.sub(
        r"```([\w\s\n$\/\-.\[\]]+)```",
        r'<div class="termy">\n\g<0>\n</div>',
        original_md,
    )
    parsed_md = parsed_md.replace(f"$ {script_name}", f"$ {script_path}")
    md_path = Path(__file__).parent.parent.joinpath(f"docs/scripts/{script_name}.md")
    md_path.write_text(parsed_md, encoding="utf8")


if __name__ == "__main__":
    app()
