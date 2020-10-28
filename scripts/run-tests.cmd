@echo off
set SQLALCHEMY_DATABASE_URL=sqlite:///testing-database.db

python app/initial_data.py
coverage run -m pytest -vv %*
