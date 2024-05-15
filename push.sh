#!/bin/bash

# Author            : Eshan Roy <eshan@snigdhaos.org>
# Author URL        : https://eshanized.github.io

check_commitizen() {
    if ! pacman -Qq commitizen-go &> /dev/null; then
        echo "Commitizen Not Found!" >&2
        exit 1
    fi
}

BRANCH=master # or 'main'/ 'development'

#
push() {
    git add .
    git cz
    git push origin -u ${BRANCH}
}

main(){
    check_commitizen
    push
}

main