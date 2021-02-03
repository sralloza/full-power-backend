# `release-changelog`

Releases a new version in the changelog.

Notes:

* Use `--no-commit` or `--nc` to disable the autocommit.
* Use `--nt` to disable the tag creation.

If the autocommit is disabled, the autotag will be disabled too, regardless of the `offline` option.

**Usage**:

<div class="termy">
```console
$ python scripts/release-changelog.py [OPTIONS] NEW_VERSION
```
</div>

**Arguments**:

* `NEW_VERSION`: [required]

**Options**:

* ` / --no-commit, --nc`: Commits the result  [default: True]
* ` / --nt`: Create tag  [default: True]
* `--offline`: Disables commit and tag  [default: False]
* `--help`: Show this message and exit.
