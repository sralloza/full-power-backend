# Docker deploy

It's recommended to deploy the backend using Docker.

You can deploy the backend using docker-compose. It will start the backend and a new database without needing you to install any database engine.

## Deploy on normal architecture

First, create a file named `backend.env` with and write this inside:

```env
MYSQL_ROOT_PASSWORD=the-password
FIRST_SUPERUSER=admin
FIRST_SUPERUSER_PASSWORD=admin
SERVER_SECRET=4aNQPLnzwNQkIqtVg4WL-TkOw_QvaGlIVkpHwd8Dv2w
```

**Note:** you can generate the `SERVER_SECRET` using `python -c "import secrets;print(secrets.token_urlsafe(32))`

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

## Develop

To create the docker images, read [docker development](../develop.md#docker).
