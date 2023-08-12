# justfile

default:
    just --list

build-and-upload: build upload

build:
    rm -rf dist
    . .venv/bin/activate
    python3 -m build

test:
    . .venv/bin/activate
    pytest

upload:
    . .venv/bin/activate
    twine upload dist/*

install-self:
    . .venv/bin/activate
    pip install -e .

init-venv:
    python3 -m venv .venv
    . .venv/bin/activate

    just install-deps

install-deps:
    . .venv/bin/activate
    pip install -r requirements.txt
