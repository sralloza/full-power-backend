FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./backendtest-oiix-ba9d6341437a.json ./requirements.txt ./alembic.ini .gitignore ./
COPY ./.git /app/.git
COPY ./scripts /app/scripts
COPY ./alembic /app/alembic
COPY ./app /app/app
COPY ./prestart.sh /app/prestart.sh
COPY ./wait-for-it.sh /app/wait-for-it.sh


ENV DIALOGFLOW_PROJECT_ID=backendtest-oiix \
    GOOGLE_APPLICATION_CREDENTIALS=./backendtest-oiix-ba9d6341437a.json \
    LOG_PATH=/logs

RUN python -m pip install --upgrade pip &&\
    pip install -r ./requirements.txt
