# Getting started

Here you have a quick introduction of the minimal setup you need to get the backend up & running.

You'll need `python 3.7+` installed to run the backend.

## Get the code

If you haven't cloned the repo follow these steps to do it.

<div class="termy">

```shell
$ git clone https://github.com/BelinguoAG/full-power-backend.git

---> 100%

$ cd full-power-backend
```

</div>

## Virtual environment

It's very recomended to create a virtual environment to separate python proyects. If you don't have one or you don't know what it is, follow this steps:

!!! note "o2switch"
    If you are deploying the backend on o2switch, you don't have to create a virtual environment, it's already created. Read [o2switch deploy instructions](deploy/deploy-o2switch.md).

=== "Linux, macOS"
    <div class="termy">

    ```python
    // Make sure virtualenv is installed
    $ python -m pip install --upgrade virtualenv
    ---> 100%

    // Create a virtualenv named ".venv"
    $ virtualenv .venv

    // Activate the virtualenv
    $ source .venv/bin/activate

    // Check it's using the virtual python binary
    $ which python
    ```

    </div>

=== "Windows"
    <div class="termy">

    ```python
    // Make sure virtualenv is installed
    $ python -m pip install --upgrade virtualenv
    ---> 100%

    // Create a virtualenv named ".venv"
    $ virtualenv .venv

    // Activate the virtualenv
    $ call .venv/scripts/activate.bat

    // Check it's using the virtual python binary
    $ where python
    ```

    </div>

## Install external libraries required

Once the python virtual environment is set up,

<div class="termy">

```shell
// Update pip just in case
python -m pip install --upgrade pip

// Install production dependencies
python -m pip install -r --upgrade requirements.txt

// If you want to develop it, install development dependencies
python -m pip install -r --upgrade requirements-dev.txt
```

</div>

## Initial Configuration

The backend settings are managed by environment variables. If you can't set environment variables you can
use the `.env` file (next to the `app` folder) to store them. The backend will load them automatically for you.

Settings needed:

- `DIALOGFLOW_PROJECT_ID`: dialogflow's project id.
- `GOOGLE_APPLICATION_CREDENTIALS`: path to the google credential's json.
- `LOG_PATH`: absolute path to the log file. The folder and the folder's parents are created at runtime.
- `LOGGING_LEVEL`: logging level. Must be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`.
- `SQLALCHEMY_DATABASE_URL`: path of the database. For sql must be like `mysql+pymysql://<user>:<password>@<host>:<port>/<table>`
- `FIRST_SUPERUSER`: first admin username. Seee the [database setup](#database-setup) for more info.
- `FIRST_SUPERUSER_PASSWORD`: first admin password. Seee the [database setup](#database-setup) for more info.

For more info about the settings, read the [settings section](settings.md).

If you don't want to mess up with the settings, you can skip that section and jump to the [database configuration](database.md).
