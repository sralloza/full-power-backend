# Scripts

Scripts are stored in the `/scripts` folder.

## Create new script

To create the script docs you need to install typer-cli (listed in `requirements-dev.txt`). You can use the script [create-scripts-docs](create-scripts-docs.md) or follow the next steps. The script executes the next steps, but automatically.

!!! tip
    It's highly recommended to use the script.

!!! danger
    Some scripts need more editing. For example, [create-first-admin](create-scripts-docs.md) has two links in the options description to the settings. Executing the command **won't** keep or create those links.

First create the script docs with the following command:

<div class="termy">
```shell
$ typer scripts/script-file-name.py utils docs --name script-file-name --output docs/scripts/script-file-name.md
```
</div>

To add the typing animation, wrap the command help inside a `div` with `class="termy"`.

Finally, edit the command help, as it says `$ xxxxx` and it should say `$ python scripts/xxxxx.py`. As it was said before, all of this can be done with the [create-scripts-docs](create-scripts-docs.md) command.
