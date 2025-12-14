# Rock-Paper-Scissors (Kivi–Paperi–Sakset)

This repository contains both:
- a terminal version of the game
- a small Flask-based web UI

## Requirements

- Python 3.12+
- Poetry

## Setup

Install dependencies:

```bash
poetry install
```

## Run the web application

Start the Flask web UI:

```bash
poetry run web
```

Then open the printed URL in your browser (typically `http://127.0.0.1:5000`).

Notes:
- If port `5000` is already in use, the app automatically picks the next free port (e.g. `5001`) and prints the actual URL.
- This is a development server intended for local use.

## Run the terminal application

```bash
poetry run python src/index.py
```

## Testing

Run the unit tests:

```bash
poetry run pytest
```

Coverage is enforced via `pytest-cov` settings in `pyproject.toml` (the test run fails if coverage drops below 100%).
