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

check-if-tag-exists:
    #!/bin/bash

    current_branch=$(git symbolic-ref --short HEAD)
    splitted_current_branch=$(echo $current_branch | tr "/" "\n")
    new_release_tag=""
    for component in $splitted_current_branch
    do
        new_release_tag=$component
    done

    version_pattern="^[0-9]+\.[0-9]+\.[0-9]+$"
    if [[ ! $new_release_tag =~ $version_pattern ]]
    then
        echo "Invalid version as a release"
        exit 41
    fi

    tags=$(git tag)
    for tag in $tags
    do
        if [ $tag = $new_release_tag ]
        then
            echo "Tag already exists"
            exit 69
        fi
    done
