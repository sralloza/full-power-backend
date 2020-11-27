# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Refactor entire application based on [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app)
- Improve bot manager

### Fixed

- Enable CI and coverage analyser

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

[unreleased]: https://github.com/BelinguoAG/full-power-backend/compare/v0.5.1...HEAD
[0.5.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/BelinguoAG/full-power-backend/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/BelinguoAG/full-power-backend/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/BelinguoAG/full-power-backend/releases/tag/v0.1.0
