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

    conda create -p ./build_env ...

Finally, for a local server that watches all changed files:

    python make.py reload


Note on branches
----------------
The source branch is the master/trunk for the actual source to generate the site, and the master branch is where
the rendered html lives (this is a result of the way github pages are done). 
