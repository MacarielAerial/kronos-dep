#!/bin/bash -e

echo "Linting YAML..."
yamllint . --strict

echo "Sorting Python import definitions..."
if [[ "${CI:=}" == "true" ]]; then
  isort . --check-only --diff
else
  isort .
fi

echo "Applying opinionated Python code style..."
if [[ "${CI:=}" == "true" ]]; then
  black . --check --diff
else
  black .
fi

echo "Checking PEP8 compliance..."
flake8 .

echo "Checking Python types..."
mypy src
mypy tests

echo "Ruffing up the code..."
if [[ "${CI:=}" == "true" ]]; then
  ruff format src --check --diff
  ruff format tests --check --diff
else:
  ruff format src
  ruff format tests

ruff check src
ruff check tests

echo "Running static analysis on code..."
semgrep --config=auto src
