import json
import re
import shutil
from pathlib import Path
from typing import List
from zipfile import ZipFile

import pandas as pd
import typer

app = typer.Typer(add_completion=False)

LANGS_SUPPORTED = {"es", "en", "fr"}


def get_dataframe(excel_path: Path) -> pd.DataFrame:
    df = pd.read_excel(excel_path.as_posix())
    if set(df.columns) != {"lang", "question", "variable"}:
        typer.secho("Invalid columns in excel", fg="bright_red")
        raise typer.Exit()

    res = df.groupby("variable").lang.apply(lambda x: set(x.values) == LANGS_SUPPORTED)
    if not res.all():
        invalid = set(res.loc[res == False].index)
        msg = f"Invalid excel file (some questions don't have all translations): {invalid}"
        typer.secho(msg, fg="bright_red")
        raise typer.Exit()

    df.set_index(["variable", "lang"], inplace=True)
    return df


def get_filenames(zip_path) -> List[str]:
    with ZipFile(zip_path) as file:
        files = file.namelist()

    files.sort()
    return files


@app.command()
def main(
    zip_path: Path = typer.Argument(
        "BackendTest.zip",
        exists=True,
        help="Zip file containing the dialogflow settings",
    ),
    excel_path: Path = typer.Argument(
        "questions.xlsx", exists=True, help="Excel with new questions"
    ),
):
    """Update the dialogflow zipfile settings with new questions from an excel file.

    It also checks the validity of the excel file, like:

    * The excel's columns must be "variable", "lang" and "question".
    * For each `variable`, there must be a question for each lang supported.
    """

    df = get_dataframe(excel_path)

    # Get the filename list
    all_filenames = get_filenames(zip_path)

    # Search for editable files
    search_pattern = re.compile(r"intents\/a\d+-[a-z-]+?(?!user_says)\.json")
    editable_files = search_pattern.findall("\n".join(all_filenames))

    # Set the new filename
    new_filename = Path(zip_path).with_name(
        zip_path.stem + ".updated" + zip_path.suffix
    )

    # Remove new file just in case
    if new_filename.exists():
        if new_filename.is_dir():
            shutil.rmtree(new_filename)
        else:
            new_filename.unlink()

    # Process file
    with ZipFile(new_filename, "w") as file_out:
        with ZipFile(zip_path) as file_in:
            # Separate editable files from non editable files
            files = set(file_in.infolist())
            editable_files = {file for file in files if file.filename in editable_files}
            non_editable_files = files - editable_files
            editable_files = sorted(editable_files, key=lambda x: x.filename)

            # Copy non editable files
            for item in non_editable_files:
                file_out.writestr(item, file_in.read(item.filename))

            # Process editable files
            for item in editable_files:
                content = file_in.read(item)
                data = json.loads(content)
                response = data["responses"][0]

                try:
                    # Get variable name
                    varname = response["affectedContexts"][0]["name"].split(
                        "-awaiting-"
                    )
                    varname = varname[-1].replace("-", "_")
                except IndexError:
                    # If the intent does not have a context, it means it's the last one
                    # so it should't be edited
                    file_out.writestr(item, file_in.read(item.filename))
                    continue

                # Update questions by language
                for lang_chunk in response["messages"]:
                    lang = lang_chunk["lang"]
                    new_text = df.loc[varname].loc[lang].iloc[0]

                    # If the old text contains a line jump, it means it's the first intent
                    # The first part should not be edited
                    if "a00" in item.filename:
                        splitted_old_text = lang_chunk["speech"][0].split("\n")
                        if len(splitted_old_text) > 1:
                            new_text = splitted_old_text[0] + "\n" + new_text

                    lang_chunk["speech"][0] = new_text

                file_out.writestr(item, json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
