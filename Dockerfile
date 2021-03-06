FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./.git /app/.git
COPY ./alembic /app/alembic
COPY ./app /app/app
COPY ./docker/gunicorn_conf.py /app/gunicorn_conf.py
COPY ./docker/prestart.sh /prestart.sh
COPY ./docker/start.sh /start.sh
COPY ./docker/wait-for-it.sh /app/wait-for-it.sh
COPY ./mega-jvki-71d99bea9a36.json ./requirements.txt ./alembic.ini .gitignore ./
COPY ./scripts /app/scripts


COPY ./docker/uvicorn /app/custom_uvicorn


RUN chmod +x /app/prestart.sh /app/wait-for-it.sh


ENV DIALOGFLOW_PROJECT_ID=mega-jvki \
    GOOGLE_APPLICATION_CREDENTIALS=./mega-jvki-71d99bea9a36.json \
    LOG_PATH=/var/log/gunicorn/backend-core.log \
    MYSQL_PORT=3306


RUN python -m pip install --upgrade pip && \
    python -m pip install -r ./requirements.txt && \
    python -m pip install /app/custom_uvicorn


VOLUME /var/log/gunicorn
