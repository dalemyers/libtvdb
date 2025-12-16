# Contributing to libtvdb

Thank you for your interest in contributing to libtvdb!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dalemyers/libtvdb.git
   cd libtvdb
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

## Running Tests

```bash
poetry run pytest
```

For coverage report:
```bash
poetry run pytest --cov=libtvdb --cov-report=html
```

## Code Quality

We use several tools to maintain code quality:

### Linting
```bash
# Ruff (fast linter)
poetry run ruff check libtvdb

# Auto-fix Ruff issues
poetry run ruff check --fix libtvdb

# Pylint (comprehensive linter)
poetry run pylint --rcfile=pylintrc libtvdb
```

### Formatting
```bash
# Check formatting
poetry run black --check libtvdb tests

# Auto-format
poetry run black libtvdb tests
```

### Type Checking
```bash
# Mypy
poetry run mypy libtvdb/

# Pyright (used by Pylance in VS Code)
poetry run pyright libtvdb
```

### Run All Checks
```bash
poetry run ruff check libtvdb && \
poetry run black --check libtvdb tests && \
poetry run pylint --rcfile=pylintrc libtvdb && \
poetry run mypy libtvdb/ && \
poetry run pyright libtvdb && \
poetry run pytest
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run all code quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8 style guidelines
- Maximum line length: 100 characters
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions focused and concise

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

## Commit Messages

- Use clear and descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Keep the first line under 72 characters
- Add detailed description if needed

## Questions?

Feel free to open an issue for any questions or concerns!
