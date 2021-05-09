"""Backend of chatbot application."""

from ._version import get_versions
from .utils.server import setup_logging

__version__ = get_versions()["version"]
del get_versions

setup_logging()

from .main import app
