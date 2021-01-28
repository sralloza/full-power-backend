# `create-first-admin`

Creates an admin. If not provided, username and password are taken from settings.

**Usage**:

<div class="termy">
```console
$ python scripts/create-first-admin.py [OPTIONS]
```
</div>

**Options**:

* `--username TEXT`: username of the admin  [default: ([settings.first_superuser](../settings.md#database))]
* `--password TEXT`: password of the admin  [default: ([settings.first_superuser_password](../settings.md#database))]
* `--help`: Show this message and exit.
