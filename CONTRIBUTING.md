# Contributing

A short guide so every member works the same way. Keep it simple.

## Setup

Run `make setup` once. It creates `.venv` and installs `requirements.txt`.

## Workflow

1. Pick a user story from `docs/backlog.md`.
2. Create a branch named after it, for example `feature/b-tire-features`.
3. Write your code as small steps and keep the stub interfaces.
4. Run `make lint` and `make test` before you push.
5. Open a pull request and fill in the template.

## Rules

- One story per branch and per pull request.
- Every function needs a type hint and a one-line docstring.
- Do not use 2025 data except for the single final test.
- Ask for one review from another member before merging.
- Do not commit data, caches or model artifacts.

## Definition of Done

- Reviewed by one other member.
- Notebook or tests run end to end.
- Docstring written.
- Docs updated if behaviour changed.
