# `clean-after-pr`

This script is designed to be executed after creating a Pull Request and merging it in GitHub.

!!! note
    You must be in the feature branch before using this script.

This script will:

1. **Fetch** the last changes to update `origin/master`
2. **Merge** `master` into `origin/master`
3. **Remove** feature branch

**Usage**:

<div class="termy">
```console
$ scripts/clean-after-pr.py [OPTIONS]
```
</div>

**Options**:

* `--help`: Show this message and exit.
