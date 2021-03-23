FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./.git /app/.git
COPY ./alembic /app/alembic
COPY ./app /app/app
COPY ./backendtest-oiix-ba9d6341437a.json ./requirements.txt ./alembic.ini .gitignore ./
COPY ./docker/prestart.sh /app/prestart.sh
COPY ./docker/wait-for-it.sh /app/wait-for-it.sh
COPY ./scripts /app/scripts


ENV DIALOGFLOW_PROJECT_ID=backendtest-oiix \
    GOOGLE_APPLICATION_CREDENTIALS=./backendtest-oiix-ba9d6341437a.json \
    LOG_PATH=/logs \
    MYSQL_PORT=3306

RUN python -m pip install --upgrade pip &&\
    pip install -r ./requirements.txt
