#!/bin/bash

pushd "${VIRTUAL_ENV}" > /dev/null

python -m pylint --rcfile=pylintrc libtvdb
python -m mypy --ignore-missing-imports libtvdb/

python -m pylint --rcfile=pylintrc tests
python -m mypy --ignore-missing-imports tests/

popd > /dev/null

