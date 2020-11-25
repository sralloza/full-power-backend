![Logo of the project](https://ingage.institute/wp-content/uploads/2020/08/GIA_LOGO.png)

<!-- <p align="center"></p> -->

# Chatbot Backend

<!-- > Additional information or tagline -->

Backend for the ingage's health chatbot application.

## Installing / Getting started

A quick introduction of the minimal setup you need to get the backend up & running.

You'll need `python 3.7+` installed to run the backend.

```shell
# First clone the repo, wether you are going to develop or deploy it.
git clone https://github.com/BelinguoAG/full-power-backend
cd full-power-backend

# If you don't have a virtualenv created, create one with:
virtualenv .venv

# Activate the virtualenv and check it's working
source <virtualenv-path>/bin/activate
which python  # check it's using the virtualenv python binary

# Install production dependencies
python -m pip install requirements.txt

# If you want to develop it, install development dependencies
python -m pip install requirements-dev.txt
```

### Initial Configuration

The backend settings are managed by environment variables. If you can't set environment variables you can
use the `.env` file (next to the `app` folder) to store them. The backend will load them automatically for you.

Settings needed:

- `DIALOGFLOW_PROJECT_ID`: dialogflow's project id.
- `GOOGLE_APPLICATION_CREDENTIALS`: path to the google credential's json.
- `LOG_PATH`: absolute path to the log file. The folder and the folder's parents are created at runtime.
- `LOGGING_LEVEL`: logging level. Must be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`.
- `SQLALCHEMY_DATABASE_URL`: path of the database. For sql must be like `mysql+pymysql://<user>:<password>@<host>:<port>/<table>`
- `FIRST_SUPERUSER`: first admin username.
- `FIRST_SUPERUSER_PASSWORD`: first admin password

After setting up the settings, you must setup the database. With the virtualenv on, execute the following commands.

```shell
# Check database connection:
python app/backend_pre_start.py

# Create database tables
python app/initial_data.py
```

## Developing

To develop the backend, first install the dependencies.

```shell
# Install production dependencies
python -m pip install requirements.txt

# If you want to develop it, install development dependencies
python -m pip install requirements-dev.txt

# Check database connection and settings are ok
python app/backend_pre_start.py

# If you don't have the database tables created, execute
python app/initial_data.py
```

You can run the app asyncrhonously (ASGI) o syncrhonously (WSGI).

```shell
# ASGI
uvicorn --port 80 --reload app:app

# WSGI
python run_windows.py
```

The tests are run with `pytest`. To run them:

```shell
pytest -vv
```

### Deploying / Publishing

This app is built using [FastAPI](https://fastapi.tiangolo.com/), a python framework to build asyncronous APIs. It normally needs an ASGI server to run, but due to compatibility (as most popular web servers like apache and nginx do not support ASGI) it includes a WSGI interface. The conversion is made thanks to [a2wsgi](https://github.com/abersheeran/a2wsgi).

### ASGI deploy

To deploy this app using ASGI you should use a linux server. FastAPI's docs recommend gunicorn to deploy the app:

```shell
# Install dependencies
pip install -r requirements.txt

# Run server
gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b :<port> app:app --reload --log-level <log-level> --access-logfile "/absolute/path/to/access.log" --error-logfile "/absolute/path/to/error.log"
```

### WSGI deploy

To deploy the backend as WSGI (like apache), you'll need a server compatible with the WSGI standard. If you are using apache, you can check the docs for [mod_wsgi](https://modwsgi.readthedocs.io/en/master/).

The server will handle the wsgi for you. If it doesn't work you can setup a really simple wsgi app:

```python
# simple-wsgi.py
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield b'Hello, World\n'
```

## Configuration

Here you should write what are all of the configurations a user can enter when
using the project.

Settings:

- `DIALOGFLOW_PROJECT_ID`: dialogflow's project id.
- `ENCRYPTION_ALGORITHM`: algorithm use to hash passwords. Default is `HS256`.
- `FIRST_SUPERUSER_PASSWORD`: first admin password.
- `FIRST_SUPERUSER`: first admin username.
- `GOOGLE_APPLICATION_CREDENTIALS`: path to the google credential's json.
- `LOG_PATH`: absolute path to the log file. The folder and the folder's parents are created at runtime.
- `LOGGING_LEVEL`: logging level. Must be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`.
- `MAX_LOGS`: max number of logs. Defaults to 30.
- `PRODUCTION`: if not present or False, the server will be running in debug mode. Defualts to False.
- `SERVER_SECRET`: 32-bytes base64 encoded token used to encrypt and decrypt JSON Web Tokens. To get a valid secret using python,
  execute `python -c "import secrets;print(secrets.token_urlsafe(32))"`.
- `SQLALCHEMY_DATABASE_URL`: path of the database. For sql must be like `mysql+pymysql://<user>:<password>@<host>:<port>/<table>`
- `TOKEN_EXPIRE_MINUTES`: number of minutes before the JSON Web Token expires.

## Troubleshooting

Common problems and how to solve them.

### Basic diagnosing tool

To check that the database is online and all the settings are ok, you can use the following script:

```shell
python app/backend_pre_start.py
```

### Permission error: 'c++' installing grpcio

It's caused by an old version of `pip`. Update `pip` using `pip install --upgrade pip` and try to install `grpcio` again.

### After the user logs in and get the token, server always returns 401

Check the header `X-Error-Reason`. If it is set to `Invalid token`, the reason behind it may be that the server is not using the same secret for each request. In the file `app/api/routes/utils.py`, comment the line `dependencies=...` as shown here:

```python
@router.get(
    "/settings",
    # dependencies=[Security(get_current_user, scopes=["admin"])],
    response_model=Settings,
)
def get_settings():
    """Returns the current api settings. Requires admin."""

    return settings
```

Then, open a couple times the route `/settings`. If each time the response shows a different `server_secret`, this is the cause.
To fix it, set your environment variable `SERVER_SECRET` or write `SERVER_SECRET=<secret>` in your env file. To get a valid secret
using python, execute `python -c "import secrets;print(secrets.token_urlsafe(32))"`.

## Contributing

This project uses the following conventions:

- [Keep a changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic versioning](https://semver.org/spec/v2.0.0.html)
- Angular's semantic commits:
  - [Official google document](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/)
  - [Angular contributing page](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
  - [Summary](https://gist.github.com/brianclements/841ea7bffdb01346392c)

## Links

Even though this information can be found inside the project on machine-readable
format like in a .json file, it's good to include a summary of most useful
links to humans using your project. You can include links like:

- Project homepage: https://github.com/BelinguoAG/full-power-backend
- Repository: https://github.com/BelinguoAG/full-power-backend
- Issue tracker: https://github.com/BelinguoAG/full-power-backendissues
- Changelog: [changelog](CHANGELOG.md)
- Related projects:
  - Backend: https://github.com/BelinguoAG/bot-frontend

## Licensing

One really important part: Give your project a proper license. Here you should
state what the license is and how to find the text version of the license.
Something like:

"The code in this project is licensed under MIT license."
