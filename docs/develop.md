# Developing

## Workflow

First of all, you should read the [contributing](contributing.md) section to know how to name commits, keep the changelog and a cople really important things more.

This proyect follows the [GitHub workflow](https://guides.github.com/introduction/flow/){: .external-link}.

One of the main rules of this workflow is to **never** create a commit in the `master` branch directly. Always create a branch (called `feature` branch) and when it's ready (after testing it) open a _Pull Request_. {>> Actually, you will create a commit in the `master` branch, but only under certain conditions and helped by an automated script. Keep reading.<<}

!!! danger
    Only create the _pull request_ when your code is ready to be deployed in the production environment. It must pass all the tests locally and have a 100% code coverage. The changelog must be updated with the new changes (under the _unreleased_ section) and docs must be updated if needed.

When opening a _Pull Request_, the tests will be automatically executed (using **Github Actions**) and **Codecov** will post a comment on the _pull request_ with a report of the code coverage. All checks must pass to merge the pull request into the `master` branch. This is a way to ensure the quality of the code.

If you creted an _issue_ before working on the pull request, you can **link** the _pull request_ and the _issue_ just by commenting on the bottom of the _pull requests_ description `Closes #xx`, where xx is the id of the _issue_. This will close the _issue_ automatically after merging the _pull request_ into `master`.

After merging the _pull request_ into master, execute the [clean-after-pr](scripts/clean-after-pr.md) script. It will downlaod the latest changes, checkout `master`, merge `master` with `origin/master` and remove the local `feature` branch (the `remote` feature branch will be removed automatically during the download with `git fetch -p`).

When your code is in the `master` branch and you have executed the last step (execute the script), you will have `master` checked out and there will be no trace of the `feature` branch. Now it's the time you ask yourself if you want to create a release. The release will cover all the changes in the _unreleased_ section of the readme. To know more about versioning, check out [semantic versioning](https://semver.org/spec/v2.0.0.html){: .external-link target="_blank"}. It will explain how to name your version and when to create said version.

If you want to create a new version, use the [release-changelog](scripts/release-changelog.md) script. Read its documentation to know how does it work. Note that the `NEW_VERSION` argument the script expects is not the tag, it's the actual version. For example, you must put {++"0.16.1"++}, not {--"v0.16.1"--} (note the v). If you don't use any option by default, it will create the commit and the tag for you automatically.

## Setup development environment

To develop the backend, first install the dependencies.

<div class="termy">

```shell
// Install production dependencies
$ python -m pip install -r --upgrade requirements.txt

// Install development dependencies also
$ python -m pip install -r --upgrade requirements-dev.txt
```

</div>

Now it's time to setup the database. Read about it [here](#database-setup).

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

The tests are the main tool to ensure the quality of the code, as long as the workflow. The tests are run with `pytest`. To run them:

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

// Now open the file htmlcov/index.html in the browser
```

</div>

The tests are automatically executed using **Github Actions** when a _pull request_ is created or a commit to `master` is pushed to the remote.

## Docker

=== "Normal"
    To build the normal image, run

    <div class="termy">
    ```shell
    $ docker build -t &lt;username&gt;/backend:&lt;tag&gt; .
    ```
    </div>

    Then you upload it to dockerhub:

    <div class="termy">
    ```shell
    $ docker push &lt;username&gt;/backend:&lt;tag&gt;
    ```
    </div>

    Then you upload it to dockerhub:

    <div class="termy">
    ```shell
    $ docker push &lt;username&gt;/backend:&lt;tag&gt;-arm
    ```
    </div>

=== "ARM"
    To build the `ARM` image, run

    <div class="termy">

    ```shell
    // Build and publish to dockerhub (recommended)
    $ docker buildx build -f Dockerfile.arm -t &lt;username&gt;/backend:&lt;tag&gt;-arm --platform=linux/arm/v7 --push .

    // Build only
    $ docker buildx build -f Dockerfile.arm -t &lt;username&gt;/backend:&lt;tag&gt;-arm --platform=linux/arm/v7 --load .
    ```

    </div>

!!! warning
    It takes a lot of time to compile, it's normal to see a bunch of messages like `Building wheel for grpcio (setup.py): still running...`. It's because grpcio doesn't provide wheels for `armv7`, so you have to compile the wheel yourself.
