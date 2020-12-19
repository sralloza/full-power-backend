# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Return `409` instead of `400` in case of id conflict creating models.

## [0.8.1] - 2020-12-14

### Fixed

- `display_type` not showing in `POST /process/process-msg` (#35).

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
- Add badges to [readme](README.md).

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

- 🔥 Add WSGI conversion.
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

[unreleased]: https://github.com/BelinguoAG/full-power-backend/compare/v0.8.1...HEAD
[0.8.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/BelinguoAG/full-power-backend/releases/tag/v0.1.0
