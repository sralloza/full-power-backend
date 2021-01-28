# Database setup

First, use the [check-db-connection script](scripts/check-db-connection.md) to check if database connection and settings are ok.

<div class="termy">
```console
$ python scripts/check-db-connection.py
```
</div>

## Upgrade database

If this is the first time you deploy the backend or you have already deployed an older version of the backend using database migrations (`alembic`) and you want to upgrade it, just execute this command to create the database's tables.

<div class="termy">
```shell
$ alembic upgrade head
```
</div>

!!! note "About migrations"
    Database migrations are managed by `alembic`. Each migration info is stored in <a href="https://github.com/BelinguoAG/full-power-backend/tree/master/alembic/versions" class="external-link" target="_blank">alembic/versions</a>. You can list them in chronological order using the history command:

    <div class="termy">
    ```shell
    $ alembic history
    bb3b26d22d3a -> 796a148a7256 (head), add files
    aa206f5fe915 -> bb3b26d22d3a, add images
    (base) -> aa206f5fe915, Add models Conversation, HealthData and User
    ```
    </div>

    In this example we have 3 diferent versions of the database:

    1. The first migration (`id=aa206f5fe915`) adds the models Conversation, HealthData and User.
    2. The second migration (`id=bb3b26d22d3a`) adds the images.
    3. The third and last migration (`id=796a148a7256`) adds the files

    Each `migration` comes with a little description of its content.

If you have already deployed a version of the backend **without** using database migrations (`alembic`), you have 2 choices:

1. **Remove all tables**. The easy solution is to remove all tables and then execute `alembic upgrade head`.
2. **Second choice: hack alembic.** If you know exactly in which point of the migration workflow you are, you can "tell" alembic the exact revision. If you are now confused or you don't now anything about migrations, I'm afraid you need to select the first solution. First, execute `alembic current`. It will output some nonesense into the terminal, but it will also create a new table in the database called `alembic_version`. You only need to set the first row of the table (**important: this table must always have one and only one row**) to the alembic revision identifier you are absolutely sure your database is at. Note that the alembic migration identifier is something like `aa206f5fe915` (you can search the `alembic/versions` folder or the `alembic history`). After you set the correct alembic revision in the database, you can execute `alembic upgrade head` safely.

## Downgrade database

If for some reason you want to undo the changes of the last migration, use the `downgrade` command.

<div class="termy">
```console
$ alembic downgrade -1
```
</div>

If you wnat to undo the last two migrations, instead of `-1` put `-2`, and so on.

## First admin settings

If this is the first time you deploy the app, the users table will be empty. To register a new admin user (with admin privileges) you need to have an existing admin user. You can create the first admin (whose username and password are set by the settings `FIRST_SUPERUSER` and `FIRST_SUPERUSER_PASSWORD`) using the [`create-first-admin`](scripts/create-first-admin.md) script:

<div class="termy">
```console
$ python scripts/create-first-admin.py
```
</div>
