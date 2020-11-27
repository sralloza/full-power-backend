import json
import os
import re
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

df = pd.read_csv("questions.csv", delimiter=";")
df.set_index(["variable", "lang"], inplace=True)
filename = Path(__file__).parent.with_name("BackendTest.zip")


# Get the filename list
with ZipFile(filename) as file:
    all_filenames = file.namelist()


# Search for editable files
search_pattern = re.compile(r"intents\/a\d+-[a-z-]+?(?!user_says)\.json")
all_filenames.sort()
editable_files = search_pattern.findall("\n".join(all_filenames))


# Set the new filename
new_filename = Path(filename).with_name(filename.stem + ".updated" + filename.suffix)


# Remove new file just in case
try:
    os.remove(new_filename)
except FileNotFoundError:
    pass


# Process file
with ZipFile(new_filename, "w") as file_out:
    with ZipFile(filename) as file_in:
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
                varname = response["affectedContexts"][0]["name"].split("-awaiting-")
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
                splitted_old_text = lang_chunk["speech"][0].split("\n")
                if len(splitted_old_text) > 1:
                    new_text = splitted_old_text[0] + "\n" + new_text

                lang_chunk["speech"][0] = new_text

            file_out.writestr(item, json.dumps(data, indent=2, ensure_ascii=False))
