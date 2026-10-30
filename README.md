# Continuous Testing & CI Quality Gates

A Python demonstration project for layered automated testing and continuous integration. It uses FastAPI, Pytest, pytest-cov, Ruff, and GitHub Actions to validate API behavior and enforce repeatable quality checks.

## Included capabilities

- Unit tests for input validation and business rules.
- Integration tests for HTTP endpoints and status codes.
- Contract tests for response structure and JSON data types.
- Regression tests for duplicate-resource protection and invalid input side effects.
- Atomic duplicate checks and thread-safe item reads/writes under concurrent requests.
- Test fixtures that restore a fixed baseline, preventing state leakage between tests.
- Positive and negative API scenarios, including validation errors, not-found, duplicate-resource cases, strict positive integer IDs, finite positive prices, and bounded item names (2–100 characters).
- CI matrix for Python 3.11 and 3.12.
- Dependency validation, linting, formatting, test execution, and an 85% coverage gate.
- JUnit XML and coverage XML artifacts retained by GitHub Actions for 14 days.

## Project structure

- `src/app.py`: FastAPI demo service.
- `tests/unit`: isolated model validation tests.
- `tests/integration`: endpoint behavior tests using FastAPI TestClient.
- `tests/contract`: response shape and type assertions.
- `tests/regression`: tests that protect previously fixed API behavior.
- `.github/workflows/quality-gates.yml`: automated CI workflow.

## Run locally

Create and activate a virtual environment, then install the development dependencies:

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
python -m pip check
ruff check src tests
ruff format --check src tests
pytest -v --cov=src --cov-report=term-missing --junitxml=junit.xml
```

The test suite enforces a minimum total coverage of 85%. This is a project-specific quality policy, not a universal industry standard.

## Run the demo API

```bash
uvicorn src.app:app --host 127.0.0.1 --port 8000
```

API documentation is available at `http://127.0.0.1:8000/docs`.

## Continuous integration

A push to `main` or a pull request targeting `main` runs the quality workflow on Python 3.11 and 3.12. Configure branch protection separately if the workflow must be required before merging.

## Scope and limitations

The API uses in-memory sample data and is intended for testing demonstrations, not production deployment. Integration tests run in-process and do not depend on external services. Workflow status is determined by actual GitHub Actions executions; no passing CI result is assumed.

## License

MIT.
