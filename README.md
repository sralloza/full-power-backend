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
python -m pip install requirements-prod.txt

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

Already covered in [Installing / Getting started](#installing--getting-started).

### Building

<p style="color: red; font-weight: bold">
TODO: fill
</p>

### Deploying / Publishing

<p style="color: red; font-weight: bold">
TODO: fill
</p>

## Features

<p style="color: red; font-weight: bold">
TODO: fill
</p>

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
