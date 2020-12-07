"""Backend of chatbot application."""

from ._version import get_versions
from .utils import setup_logging

__version__ = get_versions()["version"]
del get_versions

setup_logging()

from .main import create_app # pylint: disable=wrong-import-position

app = create_app()
