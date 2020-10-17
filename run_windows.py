"""Script designed to execute the """
from werkzeug import run_simple

from wsgi import application

run_simple('localhost', 80, application, use_reloader=True)
