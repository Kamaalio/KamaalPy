# justfile

default:
    just --list

build-and-upload: build upload

build:
    #!/bin/bash

    rm -rf dist

    . .venv/bin/activate

    python3 -m build

test:
    #!/bin/bash

    . .venv/bin/activate

    pytest

upload:
    #!/bin/bash

    . .venv/bin/activate

    twine upload dist/*

install-self:
    #!/bin/bash

    . .venv/bin/activate

    pip install -e .

init-venv:
    python3 -m venv .venv

    . .venv/bin/activate

    just install-deps

install-deps:
    #!/bin/bash

    . .venv/bin/activate

    pip install -r requirements.txt

bump-version:
    #!/bin/bash

    . .venv/bin/activate
    . scripts/utils.bash

    new_release_tag=$(extract_tag_from_release_branch)
    python scripts/bump_version.py $new_release_tag

assert-has-no-diffs:
    #!/bin/bash

    current_branch=$(git symbolic-ref --short HEAD)
    diffs=$(git diff --name-only "origin/$current_branch" | sed '/^$/d' | awk '{print NR}'| sort -nr | sed -n '1p')
    just assert-empty "$diffs"

check-if-tag-exists:
    #!/bin/bash

    . scripts/utils.bash

    new_release_tag=$(extract_tag_from_release_branch)

    version_pattern="^[0-9]+\.[0-9]+\.[0-9]+$"
    if [[ ! $new_release_tag =~ $version_pattern ]]
    then
        echo "Invalid version as a release"
        exit 41
    fi

    git fetch
    tags=$(git tag)
    for tag in $tags
    do
        if [ $tag = $new_release_tag ]
        then
            echo "Tag already exists"
            exit 69
        fi
    done

[private]
assert-empty value:
    #!/bin/bash

    . .venv/bin/activate

    python scripts/asserts/empty.py "{{ value }}"
