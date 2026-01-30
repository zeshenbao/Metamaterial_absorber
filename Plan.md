# Project Roadmap

This roadmap tracks engineering work for the refactored `metamaterial_absorber` package.

## Goals

- Maintain a stable, documented API for geometry generation.
- Keep the project installable, testable, and reproducible.
- Provide clear examples and CLI usage for portfolio review.

## Completed

- [x] Refactor into a `src/` package with a clean public API.
- [x] Add CLI entrypoint and example scripts.
- [x] Add unit tests for patterns/tiles and geometry (CadQuery).
- [x] Add CI for linting, tests, and build checks.
- [x] Update documentation for installation, usage, and testing.

## Near-term

- [ ] Add a small geometry regression fixture (tiny STL) for smoke validation.
- [ ] Add type-checking (optional `mypy`) and pre-commit hooks.
- [ ] Add changelog and release checklist.

## Long-term

- [ ] Add configuration-based pattern definitions (YAML/JSON).
- [ ] Add more patterns and cross-sections with tests.
- [ ] Publish to PyPI once API is stable.
