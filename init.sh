#! /bin/bash
# shellcheck disable=SC2164

# set -x

function init_day() {
    day="${1}"
    lang="${2:-py}"
    langs="py rs"
    if [ -z "$day" ]; then
       echo "No day supplied!" 1>&2
       exit 1
    fi

    if ! echo "$langs" | grep -wq "$lang"; then
       echo "Only allowed langs: $langs" 1>&2
       exit 1
    fi

    dir="day$day"

    if ! mkdir "$dir"; then
        echo "day $day exists. Bailing!" 1>&2
        exit 1
    fi
    pushd "$dir" || exit 1
    if ! aoc d --day "$day"; then
        echo "Failed to download. Bailing!" 1>&2
        popd || exit 1
        rm -r "$dir"
        exit 1
    fi
    echo "Creating solutions file..."
    cp "../main.template.$lang" "main.$lang" || echo "no template for lang $lang" 1>&2
    init_func="init_$lang"
    $init_func
    popd || exit 0
}

function init_py() {
    chmod +x main.py
}

function init_rs() {
    cargo init
}

init_day "$@"
