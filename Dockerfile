FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./.git /app/.git
COPY ./alembic /app/alembic
COPY ./app /app/app
COPY ./mega-jvki-71d99bea9a36.json ./requirements.txt ./alembic.ini .gitignore ./
COPY ./docker/prestart.sh /app/prestart.sh
COPY ./docker/wait-for-it.sh /app/wait-for-it.sh
COPY ./scripts /app/scripts

RUN chmod +x /app/prestart.sh /app/wait-for-it.sh

ENV DIALOGFLOW_PROJECT_ID=mega-jvki \
    GOOGLE_APPLICATION_CREDENTIALS=./mega-jvki-71d99bea9a36.json \
    LOG_PATH=/logs \
    MYSQL_PORT=3306

RUN python -m pip install --upgrade pip &&\
    pip install -r ./requirements.txt

VOLUME /var/log/gunicorn
