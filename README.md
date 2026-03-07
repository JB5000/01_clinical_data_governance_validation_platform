# 01 clinical data governance validation platform

## Objective
Industrial-grade project focused on bioinformatics/data engineering hiring signal.

## MVP Scope
- Define production-like architecture
- Implement one core end-to-end workflow
- Add tests and reproducibility guarantees
- Containerize and document execution

## Features
- Rule-based validation (not_null, between, regex)
- Compliance reporting
- REST API with FastAPI
- Docker containerization
- CI/CD with GitHub Actions

## Installation
```bash
pip install -e .
```

## Usage
Run API: `uvicorn src.main:app --reload`

Run tests: `pytest`

Build Docker: `docker build -t clinical-validation .`

## Folder Layout
- src/: application modules
- tests/: unit/integration tests
- configs/: YAML/TOML settings
- docs/: architecture, ADRs, runbooks
- data/raw and data/processed: local data boundaries
- scripts/: automation helpers

## First Build Steps
1. Write architecture in docs/architecture.md
2. Add initial config in configs/
3. Implement minimal vertical slice in src/
4. Add one integration test in tests/
5. Add Dockerfile + CI workflow

## MVP Progress
- Added rule-engine style validation for not-null, range, and regex checks.
- Added compliance summary utility for audit-ready metrics.
- Added REST API for validation.
- Added Docker and CI.
- Added tests for core governance logic.
