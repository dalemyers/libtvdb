# libtvdb

[![CI](https://github.com/dalemyers/libtvdb/workflows/CI/badge.svg)](https://github.com/dalemyers/libtvdb/actions)
[![PyPI version](https://badge.fury.io/py/libtvdb.svg)](https://badge.fury.io/py/libtvdb)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A wrapper around the [TVDB API](https://api.thetvdb.com/swagger).

## Installation

```bash
pip install libtvdb
```

## Examples

Searching for shows:

```python
import libtvdb

client = libtvdb.TVDBClient(api_key="...", pin="...")
shows = client.search_show("Doctor Who")

for show in shows:
    print(show.name)
```

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linters and type checkers
poetry run ruff check libtvdb
poetry run black --check libtvdb tests
poetry run pylint libtvdb
poetry run mypy libtvdb
poetry run pyright libtvdb
```

## Advanced

You can set `libtvdb_api_key` and `libtvdb_pin` in your OS X keychain if you don't want to supply these every time. If any of the values supplied to the `TVDBClient` constructor are `None`, it will look into your keychain and load the appropriate value. If it can't find them, it will throw an exception.
