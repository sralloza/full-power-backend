# Changelog

All notable changes to this project will be documented in this file.

The format is based on <a href="https://keepachangelog.com/en/1.0.0/" class="external-link" target="_blank">Keep a Changelog</a>,
and this project adheres to <a href="https://semver.org/spec/v2.0.0.html" class="external-link" taget="_blank">Semantic Versioning</a>.

## [Unreleased]

## [1.0.2] - 2021-05-13

### Changed

- Add `401` examples on private routes.

## [1.0.1] - 2021-05-13

### Fixed

- Pinned pydantic to 1.8.2 and fastapi to 0.65.1 to fix pydantic's security fix.

## [1.0.0] - 2021-05-09

### Added

- Endpoints to create and retrieve multiples files at once (`/files/multi`).
- Endpoint to list the files grouped by language (`/files/all`)
- A `POST`, `PUT` or `DELETE` request to `/files` will trigger the image outdated detection (if an image is not referenced in any file, it will be automatically removed).
- Add docker support.

### Changed

- *Interactive* docs are now in `/idocs` (previously in `/docs`) and *redoc* docs are now in `/docs` (previously in `/redoc`).
- Disable only *interactive* docs (`/idocs`) in **production**.
- Pinned dependencies.

### Fixed

- Fix `codecov`'s flags.
- Catch `dialogflow` permission errors
- Fixed _Bot sends some questions twice_
- Fixed _Bot responses (questions) are too big for the table's column_
- Improve checks in changelog script.

### Removed

- Disable logs rolling.
- Settings `max_logs`.

## [0.13.0] - 2021-02-25

### Added

- Add endpoint `/notifications-content/second-survey/{problem}`.
- Add endpoint `/notifications-content/generic`.
- Add setting `bot_question_message_flag`.
- Add support to `python 3.9`.

### Changed

- Add parameter `question_response` to endpoint `/process-msg`.
- Enable second survey questions (echo).
- Enable second survey responses.
- Send header `X-Problems-Parsed` in the last step of `/process-msg` endpoint.
- Send header `X-Health-Data-Result` in the last step of `/process-msg` endpoint.

## [0.12.0] - 2021-02-14

### Changed

- Changed Health Data algorithm. Now considers two classes of real problems: `light` and `serious`.
- Show user's problem report in a new message in the chat.

### Fixed

- Error message in `File.name` validation.

### Removed

- Removed `settings.problem_ratio_threshold`

## [0.11.1] - 2021-02-12

### Fixed

- Script `release-changelog` fails creating a tag.

## [0.11.0] - 2021-02-12

### Added

- Add docs page.
- Send the contents of `/me` in the HTTP header `X-Current-User` as json in `/login`.
- Add attribute to **User** model: `accepted_disclaimer`
- Add attribute to **User** model: `filled_survey`
- Add endpoint to set **User.accepted_disclaimer**: `/accept-disclaimer`
- Add endpoint to set **User.filled_survey**: `/survey-filled`

### Changed

- Script `update-questions` needs an excel file, not a csv one.
- Improve scripts using `typer`.

### Fixed

- `/me` should not return the `user_id`.

## [0.10.0] - 2021-01-30

### Added

- Add attribute `user.last_login`.
- Add script `create-scripts-docs`.

### Changed

- Bump `fastapi` version to `0.63.0`.
- Improve `requirements` management.
- Endpoint `/bot/process-msg` returns a list of the bot's messages in the `bot_msg` attribute.
- **Internal** refactoring.

## [0.9.0] - 2020-12-22

### Added

- Add new setting: `problem_ratio_threshold`

### Changed

- When processing a complete HealthData, now it identifies real problems using the setting `problem_ratio_threshold` and explains them in the returned string.
- Return `409` instead of `400` in case of id conflict creating models.
- Make `POST /image` return `415` if image processing fails. ([#38](https://github.com/sralloza/full-power-backend/issues/38))
- Return `201` instead of `200` on model creation.
- Return `404` in endpoints which returns a user attribute if the user does not exist.

## [0.8.1] - 2020-12-14

### Fixed

- `display_type` not showing in `POST /process/process-msg`. ([#35](https://github.com/sralloza/full-power-backend/issues/35))

## [0.8.0] - 2020-12-07

### Added

- CRUD routes for managing files.
- CRUD routes for managing images.
- Cover every schema with tests.

### Changed

- Improve documentation.
- Improve CRUD pattern.
- Improve schemas.
- Remove testing database before each unit test.
- Pin requirements versions

### Fixed

- Check for username validity before registering a new user.

## [0.7.1] - 2020-11-30

### Fixed

- Remove "v" from version name (#27).

## [0.7.0] - 2020-11-29

### Added

- Set up database migrations.

## [0.6.0] - 2020-11-27

### Added

- Setup github actions (CI) and codecov as coverage analyser.
- Add badges to readme.

### Changed

- Refactor entire application based on [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app)
- Improve bot manager

### Fixed

- Enable CI and coverage analyser

### Fixed

- Rollback database if error detected.

## [0.5.1] - 2020-10-24

### Fixed

- Fix permission error when doing a log rollover.

## [0.5.0] - 2020-10-22

### Added

- Add route `/refresh` to refresh tokens.
- Add scopes to tokens.
- Add setting `TOKEN_EXPIRE_MINUTES`.

## [0.4.1] - 2020-10-21

### Fixed

- Fix route DELETE `/users/<id>`.

## [0.4.0] - 2020-10-21

### Added

- Add `LOG_PATH`, `MAX_LOGS` and `LOGGING_LEVEL` settings.
- Add routes `/` and `/version`.
- Enable logging.
- Log critical errors.

### Changed

- Improve login error messages via `X-Error-Reason` header.
- Move app declaration to `app.main`.
- Return token expiration time in `/login` with the token.

## [0.3.1] - 2020-10-21

### Fixed

- Specify `/settings` return model.

## [0.3.0] - 2020-10-20

### Added

- ???? Add WSGI conversion.
- Add `/settings` route to retrieve settings.

### Changed

- Manage `dialogflow` data via settings.

### Fixed

- Specify table's fields length to be compatible with sql.

## [0.2.0] - 2020-10-18

### Changed

- Use `pydantic`'s `BaseSettings` to manage settings.

## [0.1.0] - 2020-10-18

### Added

- First version

[unreleased]: https://github.com/sralloza/full-power-backend/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/sralloza/full-power-backend/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/sralloza/full-power-backend/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/sralloza/full-power-backend/compare/v0.13.0...v1.0.0
[0.13.0]: https://github.com/sralloza/full-power-backend/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/sralloza/full-power-backend/compare/v0.11.1...v0.12.0
[0.11.1]: https://github.com/sralloza/full-power-backend/compare/v0.11.0...v0.11.1
[0.11.0]: https://github.com/sralloza/full-power-backend/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/sralloza/full-power-backend/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/sralloza/full-power-backend/compare/v0.8.1...v0.9.0
[0.8.1]: https://github.com/sralloza/full-power-backend/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/sralloza/full-power-backend/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/sralloza/full-power-backend/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/sralloza/full-power-backend/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/sralloza/full-power-backend/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/sralloza/full-power-backend/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/sralloza/full-power-backend/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/sralloza/full-power-backend/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/sralloza/full-power-backend/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/sralloza/full-power-backend/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/sralloza/full-power-backend/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/sralloza/full-power-backend/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/sralloza/full-power-backend/releases/tag/v0.1.0
