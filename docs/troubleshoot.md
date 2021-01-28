# Troubleshooting

Common problems and how to solve them.

## Basic diagnosing tool

To check that the database is online and all the settings are ok, you can use the [check-db-connection script](scripts/check-db-connection.md):

<div class="termy">
```shell
$ python scripts/check-db-connection.py
```
</div>

## ModuleNotFoundError: No module named 'app'

You need to install the app to make it importable. Execute `python -m pip install .` at the root folder, next to the `readme.md` file.

## Permission error: 'c++' installing grpcio

It's caused by an old version of `pip`. Update `pip` using `python -m pip install --upgrade pip` and try to install `grpcio` again.

## After the user logs in and get the token, server always returns 401

Check the header `X-Error-Reason`. If it is set to `Invalid token`, the reason behind it may be that the server is not using the same secret for each request. In the file `app/api/routes/utils.py`, comment the line `dependencies=...` as shown here:

```python hl_lines="3"
@router.get(
    "/settings",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_model=Settings,
)
def get_settings():
    """Returns the current api settings. Requires admin."""

    return settings
```

Then, open a couple times the route `/settings`. If each time the response shows a different `server_secret`, this is the cause.
To fix it, set your environment variable `SERVER_SECRET` or write `SERVER_SECRET=<secret>` in your env file. To get a valid secret
using python, execute `python -c "import secrets;print(secrets.token_urlsafe(32))"`.
