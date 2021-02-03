# `update-questions`

Update the dialogflow zipfile settings with new questions from an excel file.

It also checks the validity of the excel file, like:

* The excel's columns must be "variable", "lang" and "question".
* For each `variable`, there must be a question for each lang supported.

**Usage**:

<div class="termy">
```console
$ python scripts/update-questions.py [OPTIONS] [ZIP_PATH] [EXCEL_PATH]
```
</div>

**Arguments**:

* `[ZIP_PATH]`: Zip file containing the dialogflow settings  [default: BackendTest.zip]
* `[EXCEL_PATH]`: Excel with new questions  [default: questions.xlsx]

**Options**:

* `--help`: Show this message and exit.
