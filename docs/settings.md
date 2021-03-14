# Settings

Settings are managed with environment variables. You can set the enviroment variables or use the `.env` file. The `.env` file must be placed in the root folder.

!!! note
    The environment variables and the `.env` file don't have to be all upercase. It's case insensitive.

Here is a list of all the settings clasified by category.

!!! note
    Required settings are marked with 🚩.

## General

- `production`: if not present or `False`, the server will be running in debug mode. If it's True the documentation will be deactivated. Defaults to `False`.

## Security

- `encryption_algorithm`: algorithm use to hash passwords. Don't change this unless you are 100% sure. Default is `HS256`.
- `server_secret`: 32-bytes base64 encoded token used to encrypt and decrypt JSON Web Tokens. To get a valid secret using python, execute `python -c "import secrets;print(secrets.token_urlsafe(32))"`. It's defined in runtime, but it's possible that for each request the token is redifined, so all JSON Web Tokens will be invalid. Therefore, it's very encouraged to define it.
- `token_expire_minutes`: number of minutes before the JSON Web Token expires. Defaults to 30 minutes.

## Database

- 🚩 `first_superuser_password`: first admin password. See the [database setup](database.md#first-admin-settings) for more info.
- 🚩 `first_superuser`: first admin username. See the [database setup](database.md#first-admin-settings) for more info.
- 🚩 `sqlalchemy_database_url`: path of the database. For sql must be like `mysql+pymysql://<user>:<password>@<host>:<port>/<table>`

## Dialogflow

- 🚩 `dialogflow_project_id`: dialogflow's project id.
- 🚩 `google_application_credentials`: path to the google credential's json.

## Logging

- 🚩 `log_path`: absolute path to the log file. The folder and the folder's parents are created at runtime.
- `logging_level`: logging level. Must be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Defaults to `INFO`.

## Bot generics

- `bot_split_char`: string to separate messages of the bot besides `\n`. Defaults to `~`.

!!! example "settings.bot_split_char"
    If dialogflow's chatbot responds with `"hi there\nI'm here~But not there"` the backend will parse that output as `["hi there", "I'm here", "But not there"]`.

!!! warning
    This setting must be in sync with the questions excel and the chatbot's questions.

- `bot_question_message_flag`: string to define the messages trigerred by the notification. It will just echo the input message. Defaults to `<NOTIFICATION_QUESTION>`.

## Testing

- `username_test_user`: test user's username. It's only used during tests. Defaults to `the_Test`.
- `username_test_password`: test user's password. It's only used during tests. Defaults to `the_TestPassword`.
