set export

@_default:
    just --list


bootstrap:
    git submodule update --init --recursive
    if test ! -e .venv; then \
      uv venv && uv pip install -r requirements.txt ; \
    fi
    pre-commit install

check-prettier:
    prettier "docs/**/*.md" --check

do-prettier:
    prettier -w "docs/**/*.md"


check-ruff:
    ruff check runner/
    ruff format --check runner/

do-ruff:
    ruff format runner/

test-all:
    pytest

