#!/usr/bin/env conda-execute

# conda execute
# env:
#  - python 
#  - pelican
#  - markdown
#  - ipython >=3,<4
#  - ipython-notebook
# channels:
#  - asmeurer
#  - IOOS
# run_with: python

import os
import glob
import shutil
import subprocess


def html():
    cmd = ['pelican', 'content', '--output', 'output', '--settings', 'pelicanconf.py']
    subprocess.check_call(cmd)


def reload():
    cmd = ['pelican', 'content', '--autoreload', '--output', 'output',
           '--settings', 'pelicanconf.py']
    subprocess.check_call(cmd)


def publish():
    cmd = ['pelican', 'content', '--output', 'output',
           '--settings', 'publishconf.py']
    subprocess.check_call(cmd)
    # Remove all ordinary files (not .git/.nojekyl though)
    for fname in glob.glob('output_branch/*'):
        if os.path.isdir(fname):
            shutil.rmtree(fname)
        else:
            os.unlink(fname)
    # Copy all files
    for fname in glob.glob('output/*'):
        if os.path.isdir(fname):
            shutil.copytree(fname, os.path.join('output_branch', os.path.basename(fname)))
        else:
            shutil.copy(fname, os.path.join('output_branch', os.path.basename(fname)))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('Help')
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    parser_html = subparsers.add_parser('html', help="Make the html")
    parser_html.set_defaults(func=html)

    parser_publish = subparsers.add_parser('publish', help="Make publishable html, and put it in the output_branch.")
    parser_publish.set_defaults(func=publish)

    parser_reload = subparsers.add_parser('reload', help="Make the html, and watch the folder for any changes.")
    parser_reload.set_defaults(func=reload)

    args = parser.parse_args()
    args.func()
