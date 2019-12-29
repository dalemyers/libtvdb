#!/bin/bash

pushd "${VIRTUAL_ENV}" > /dev/null

source "${VIRTUAL_ENV}/bin/activate"

python -m black --line-length 100 libtvdb tests
python -m pylint --rcfile=pylintrc libtvdb tests
python -m mypy --ignore-missing-imports libtvdb/ tests/

popd > /dev/null

