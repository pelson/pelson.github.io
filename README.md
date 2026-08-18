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

Next, create an environment:

    uv venv ./venv
    source ./venv/bin/activate
    uv pip install -r requirements.txt ./extras/liquid-tags

To run a local server that watches all changed files:

    uv run --no-project --with-requirements ./requirements.txt python make.py reload

To update the requirements.txt:

   uv pip compile requirements.in | grep -v pelican-liquid-tags > requirements.txt 


