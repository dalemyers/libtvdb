#!/usr/bin/env pwsh

python -m black --line-length 100 libtvdb tests
python -m pylint --rcfile=pylintrc libtvdb tests
python -m mypy --ignore-missing-imports libtvdb/ tests/
