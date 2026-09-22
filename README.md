[![Build Status](https://travis-ci.org/pelson/pelson.github.io.svg?branch=source)](https://travis-ci.org/pelson/pelson.github.io)

This is the blog of @pelson which can be viewed at [pelson.github.io](https://pelson.github.io).
If you'd like to get in touch with me, check out the blog and you will find my contact information.

## Building locally

First, clone this repository and its submodules:

    git clone --recursive git@github.com:pelson/pelson.github.io.git
    cd pelson.github.io

OR

    git clone git@github.com:pelson/pelson.github.io.git
    cd pelson.github.io
    git submodule update --init --recursive

Dependencies are managed with [uv](https://docs.astral.sh/uv/); no separate environment setup is needed.

To run a local server that watches all changed files:

    ./make.py reload

(`make.py` is a `uv run` script, so this resolves `requirements.txt` and Python 3.13 on demand.)

To update requirements.txt after changing pyproject.toml:

    uv pip compile pyproject.toml -o requirements.txt


