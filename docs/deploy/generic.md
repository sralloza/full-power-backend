# Deploying / Publishing

This app is built using [FastAPI](https://fastapi.tiangolo.com/), a python framework to build asyncronous APIs. It normally needs an ASGI server to run, but due to compatibility (as most popular web servers like apache and nginx do not support ASGI) it includes a WSGI interface. The conversion is made thanks to [a2wsgi](https://github.com/abersheeran/a2wsgi).

If you haven't setup the database already, now it's time. Check the [instructions](#database-setup).

## ASGI deploy

To deploy this app using ASGI you should use a linux server. <a href="https://fastapi.tiangolo.com/deployment/manually/" class="external-link" target="_blank">FastAPI's docs</a> recommend gunicorn to deploy the app:

!!! quote "Explanation of ASGI from its <a href="https://asgi.readthedocs.io/en/latest/" class="external-link" target="_blank">docs</a>"
    ASGI (Asynchronous Server Gateway Interface) is a spiritual successor to WSGI, intended to provide a standard interface between async-capable Python web servers, frameworks, and applications.

    Where WSGI provided a standard for **synchronous** Python apps, ASGI provides one for both **asynchronous** and **synchronous** apps, with a WSGI backwards-compatibility implementation and multiple servers and application frameworks.

<div class="termy">

```console
// Install dependencies
$ pip install -r --upgrade requirements.txt

// Run server
$ gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b :<port> app:app --reload --log-level <log-level> --access-logfile "/absolute/path/to/access.log" --error-logfile "/absolute/path/to/error.log"
```

</div>

## WSGI deploy

To deploy the backend as <a href="https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface" class="external-link" target="_blank">WSGI</a> (like <a href="https://httpd.apache.org/" class="external-link" target="_blank">Apache</a>), you'll need a server compatible with the WSGI standard. If you are using apache, you can check the docs for <a href="https://modwsgi.readthedocs.io/en/master/" class="external-link" target="_blank">mod_wsgi</a>.

!!! quote "Explanation of WSGI from its <a href="https://wsgi.readthedocs.io/en/latest/what.html" class="external-link" target="_blank">docs</a>"
    WSGI is the Web Server Gateway Interface. It is a specification that describes how a web server communicates with web applications, and how web applications can be chained together to process one request.

    WSGI is a Python standard described in detail in <a href="https://www.python.org/dev/peps/pep-3333/" class="external-link" target="_blank">PEP 3333</a>.

    For more, see <a href="https://wsgi.readthedocs.io/en/latest/learn.html" class="external-link" target="_blank">Learn about WSGI</a>.

The server will handle the wsgi for you. If it doesn't work you can setup a really simple wsgi app:

```python
# simple-wsgi.py
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield b'Hello, World\n'
```

### Apache example

Asuming you have cloned the repo to `/srv/full-power-backend`:

```apacheconf
<VirtualHost *:80>
    ServerName backend.example.es

    WSGIScriptAlias / /srv/full-power-backend/wsgi.py

    <Directory /srv/full-power-backend/>
        Options +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

??? warning "Mod Security"
    If you have Mod Security available, don't forget to disable the rule `911100`. Just insert this line inside the virtualhost tag:

    ```apacheconf hl_lines="14"
    <VirtualHost *:80>
        ServerName backend.example.es

        WSGIScriptAlias / /srv/full-power-backend/wsgi.py

        <Directory /srv/full-power-backend/>
            Options +FollowSymLinks
            AllowOverride None
            Require all granted
        </Directory>

        SecRuleRemoveById 911100
    </VirtualHost>
    ```
