import re
import subprocess
from io import StringIO
from pathlib import Path
from typing import Generator

import click
import typer
from ruamel.yaml import YAML

app = typer.Typer(add_completion=False)
yaml_path = Path(__file__).parent.parent / "mkdocs.yml"


def check_script_name(script_name: str):
    if script_name is None:
        return None
    if not Path(__file__).with_name(script_name + ".py").is_file():
        raise typer.BadParameter(f"Script 'scripts/{script_name}.py doesn't exist")
    return script_name


def update_docs(script_name: str):
    script_path = f"scripts/{script_name}.py"
    args = ["typer", script_path, "utils", "docs", "--name", script_name]

    r = subprocess.run(args, capture_output=True)
    original_md = r.stdout.decode("utf8").replace("\r\n", "\n").strip() + "\n"
    parsed_md = re.sub(
        r"```([\w\s\n$\/\-.\[\]]+)```",
        r'<div class="termy">\n\g<0>\n</div>',
        original_md,
    )
    parsed_md = parsed_md.replace(f"$ {script_name}", f"$ python {script_path}")
    md_path = Path(__file__).parent.parent.joinpath(f"docs/scripts/{script_name}.md")
    md_path.write_text(parsed_md, encoding="utf8")


def check_yaml_file():
    if not yaml_path.is_file():
        raise click.ClickException(
            "mkdocs.yml does not exist [%r]" % yaml_path.as_posix()
        )


def get_all_scripts() -> Generator[Path, None, None]:
    for file in Path(__file__).parent.iterdir():
        if file.suffix == ".py":
            yield file


def update_yaml(script_name: str):
    yaml = YAML(typ="rt")
    yaml.indent(mapping=2, sequence=4, offset=2)

    with yaml_path.open(encoding="utf8") as fh:
        mkdocs_data = yaml.load(fh)

    if "nav" not in mkdocs_data:
        mkdocs_data["nav"] = list()

    nav = mkdocs_data["nav"]
    for item in nav:
        if list(item.keys())[0] == "Scripts":
            scripts_nav = item["Scripts"]
            break
    else:
        nav.append({"Scripts": []})
        scripts_nav = nav[0]["Scripts"]

    if scripts_nav and "intro" in list(scripts_nav[0].keys())[0].lower():
        intro = scripts_nav.pop(0)
    else:
        intro = None

    known_scripts = list(list(x.keys())[0] for x in scripts_nav)

    if script_name not in known_scripts:
        scripts_nav.append({script_name: f"scripts/{script_name}.md"})

    scripts_nav.sort(key=lambda x: list(x.keys())[0])

    if intro:
        scripts_nav.insert(0, intro)

    buffer = StringIO()
    yaml.dump(mkdocs_data, buffer)

    yaml_str = buffer.getvalue()
    yaml_str = yaml_str.replace("%21", "!")
    yaml_path.write_text(yaml_str, encoding="utf8")


@app.command()
def main(
    script_name: str = typer.Argument(
        None,
        help="Name of the script without extension. If not passed,"
        " it will create the docs for all the scripts.",
        callback=check_script_name,
    )
):
    """Updates the docs for a script."""
    if script_name is None:
        scripts = list(get_all_scripts())
        typer.echo("Updating all scripts")
    else:
        scripts = [Path(script_name)]

    check_yaml_file()

    for script in scripts:
        update_docs(script.stem)
        update_yaml(script.stem)


if __name__ == "__main__":
    app()
