#!/bin/bash

function extract_tag_from_release_branch()
{
    current_branch=$(git symbolic-ref --short HEAD)
    splitted_current_branch=$(echo $current_branch | tr "/" "\n")
    new_release_tag=""
    for component in $splitted_current_branch
    do
        new_release_tag=$component
    done

    echo $new_release_tag
}
