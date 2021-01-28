# Developing

To develop the backend, first install the dependencies.

<div class="termy">

```shell
// Install production dependencies
$ python -m pip install -r --upgrade requirements.txt

// If you want to develop it, install development dependencies
$ python -m pip install -r --upgrade requirements-dev.txt
```

</div>

Now, it's time to setup the database. Read about it [here](#database-setup).

You can run the app asyncrhonously (ASGI) o syncrhonously (WSGI).

<div class="termy">

```shell
// ASGI
$ uvicorn --port 80 --reload app:app

// WSGI
$ python run_windows.py
```

</div>

## Tests

The tests are run with `pytest`. To run them:

<div class="termy">
```shell
$ pytest -vvl
```
</div>

Coverage is managed by `coverage`:

<div class="termy">

```console
$ python -m coverage run -m pytest -vvl

// Create coverage report in html
$ python -m coverage html
```
</div>
