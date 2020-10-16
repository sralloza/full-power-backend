import sys
from pathlib import Path
from platform import system

try:
    from a2wsgi import ASGIMiddleware
except ImportError:
    print("Install a2wsgi with 'pip install a2wsgi'", sys.stderr)
    sys.exit(1)

if system() == "Windows":
    activate_this_path = ".venv/scripts/activate_this.py"
else:
    activate_this_path = ".venv/bin/activate_this.py"

activate_this_path = Path(__file__).parent.joinpath(activate_this_path)
with activate_this_path.open() as file:
    exec(file.read(), dict(__file__=activate_this_path.as_posix()))


sys.path.insert(0, Path(__file__).parent.as_posix())
from app import app

application = ASGIMiddleware(app)
