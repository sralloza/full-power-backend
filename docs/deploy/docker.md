# Docker deploy

It's recommended to deploy the backend using Docker.

You can deploy the backend using docker-compose. It will start the backend and a new database without needing you to install any database engine.

## Deploy on normal architecture

First, create a file named `backend.env` with and write this inside:

```env hl_lines="5-6"
MYSQL_ROOT_PASSWORD=the-password
FIRST_SUPERUSER=admin
FIRST_SUPERUSER_PASSWORD=admin
SERVER_SECRET=4aNQPLnzwNQkIqtVg4WL-TkOw_QvaGlIVkpHwd8Dv2w
ACCESS_LOG=/var/log/gunicorn/backend-access.log
ERROR_LOG=/var/log/gunicorn/backend-error.log
```

**Note:** you can generate the `SERVER_SECRET` using `python -c "import secrets;print(secrets.token_urlsafe(32))`

**Note 2:** as for the 2 highlighted lines, read the [logs](#logs) section.

And then use `docker-compose`. It's that simple.

<div class="termy">
```shell
$ docker-compose up -d
```
</div>

To shutdown:

<div class="termy">
```shell
$ docker-compose down
```
</div>

## Deploy on ARM architecture (raspberry pi)

You can't deploy the app using the default docker-compose. You will need a special docker-compose with ARM

<div class="termy">
```shell
$ docker-compose -f docker-compose.arm.yml up -d
```
</div>

To shutdown:

<div class="termy">
```shell
$ docker-compose -f docker-compose.arm.yml down
```
</div>

## Logs

According to the `backend.env` example, the backend will store the logs in `/var/log/gunicorn`. To access them in the host, the `docker-compose` files will create a link between the container's `/var/log/gunicorn` and the host's `./logs`

=== "Normal"
    ```yaml hl_lines="12-13"
    --8<--- "./docker-compose.yml"
    ```

=== "ARM"
    ```yaml hl_lines="12-13"
    --8<--- "./docker-compose.arm.yml"
    ```

Note: **don't** set the logs environment variables to point to another folder, because the `dockerfile`s are designed to only make `/var/log/gunicorn` visible (as a volume). You can see it looking the code from the dockerfiles.

=== "Normal"
    ```Dockerfile hl_lines="20"
    --8<--- "./Dockerfile"
    ```

=== "ARM"
    ```Dockerfile hl_lines="24"
    --8<--- "./Dockerfile.arm"
    ```

## Develop

To create the docker images, read [docker development](../develop.md#docker).
