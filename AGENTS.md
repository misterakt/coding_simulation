# Repository Guidelines

## Project Structure & Module Organization

This repository is currently a lightweight sandbox for coding tests and idea simulation. The root contains `README.md` and Python-oriented ignore rules in `.gitignore`; no source package, test suite, or build configuration is checked in yet.

When adding implementation code, keep it under a clear top-level package such as `src/` or a named project module. Place tests in `tests/` with paths that mirror the source layout. Keep generated artifacts, virtual environments, coverage output, and caches out of Git; the existing `.gitignore` already excludes common Python build and runtime files.

## Build, Test, and Development Commands

There is no project-specific build system yet. Add commands to this section when introducing tooling, and prefer standard Python entry points.

Useful baseline commands:

- `python -m venv .venv`: create a local virtual environment.
- `source .venv/bin/activate`: activate the environment on macOS/Linux.
- `python -m pytest`: run tests once `pytest` and a `tests/` directory are added.
- `python -m compileall .`: perform a basic syntax check for Python files.

## Coding Style & Naming Conventions

Use Python conventions unless a different stack is explicitly introduced. Prefer 4-space indentation, `snake_case` for functions and variables, `PascalCase` for classes, and lowercase module names. Keep modules focused and avoid committing experiment output or local scratch files.

If formatters or linters are added, document them here and run them before opening a pull request. Common choices are `ruff`, `black`, and `mypy`, but do not assume they are available until configuration files are committed.

## Testing Guidelines

Put tests under `tests/` and name files `test_*.py`. Write focused unit tests for reusable functions and add regression tests for bug fixes. For experiments, include a short test or reproducible command when behavior matters.

## Commit & Pull Request Guidelines

The Git history currently contains only `Initial commit`, so no strict convention is established. Use short, imperative commit messages such as `Add parser test fixture` or `Document setup commands`.

Pull requests should include a concise summary, the commands run for verification, and any relevant context for future contributors. Link issues when applicable and include screenshots only for user-visible UI changes.

## Security & Configuration Tips

Do not commit secrets, local credentials, databases, or `.env` files. Document required environment variables in `README.md` or an example config file instead.
