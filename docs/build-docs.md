# How to build the docs

You need the external libraries `mkdocs-material` and `markdown-include`. Both are listed in `requirements.txt`. After installing both, you can either use the docs [locally](#local-docs) or [deploy them](#deploy-docs).

## Local docs

You can run a simple server to host the docs on your machine. Execute the following command to do it.

<div class="termy">
```shell
$ mkdocs -m serve -a 127.0.0.1:80
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 1.16 seconds
[I 210126 11:14:10 server:335] Serving on http://127.0.0.1:80
[I 210126 11:14:10 handlers:62] Start watching changes
INFO    -  Start watching changes
[I 210126 11:14:10 handlers:64] Start detecting changes
INFO    -  Start detecting changes
```
</div>

!!! note "Port"
    You can change the port to whatever number you want.

## Deploy docs

<div class="termy">
```shell
$ mkdocs build
```
</div>

The `build` command will create a new folder, `site`. It contains the static files of the doc's page, so you will need to deploy it using some server. For example, you can *"deploy"* it using python. Just enter the folder and type `python -m http.server 80` (it's not a production deploy, just a test deploy).

### Apache

If you haven't read the [deployment instructions](deploy/generic.md#apache-example), do it before continuing.

If you want to deploy the backend and the docs using Apache, you can copy the `site` folder (which contains the static files of the docs page) to another folder. In this example the `site` folder would be copied to `/srv/full-power-backend-docs`.

```apacheconf hl_lines="12 14-16"
<VirtualHost *:80>
    ServerName backend.example.es

    WSGIScriptAlias / /srv/full-power-backend/wsgi.py

    <Directory /srv/full-power-backend/>
        Options +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    Alias bdocs/ /srv/full-power-backend-docs

    <Directory /srv/full-power-backend-docs/>
        Require all granted
    </Directory>
</VirtualHost>
```

!!! tip "Password protected docs"
    With apache, you can restrict the access to the page.

    The first step is to create a user. It will write the username and the hashed password to a file. This example will create the user `test` in the file `/srv/.passwords/backend-docs`.

    <div class="termy">
    ```shell
    // Only include the '-c' if the file is new
    $ htpasswd -c /srv/.passwords/backend-docs test
    New password:
    Re-type new password:
    Adding password for user test
    ```
    </div>

    Once the file is created, you can alter the virtualhost configuration of apache.

    ```apacheconf hl_lines="15-19"
    <VirtualHost *:80>
        ServerName backend.example.es

        WSGIScriptAlias / /srv/full-power-backend/wsgi.py

        <Directory /srv/full-power-backend/>
            Options +FollowSymLinks
            AllowOverride None
            Require all granted
        </Directory>

        Alias bdocs/ /srv/full-power-backend-docs

        <Directory /srv/full-power-backend-docs/>
            AuthType Basic
            AuthName "Backend docs"
            AuthBasicProvider file
            AuthUserFile /srv/.passwords/backend-docs
            Require valid-user
        </Directory>
    </VirtualHost>
    ```
