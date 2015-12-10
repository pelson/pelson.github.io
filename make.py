#!/usr/bin/env conda-execute

# conda execute
# env:
#  - python 
#  - pelican
#  - markdown
#  - ipython
#  - ipython-notebook
#  - tidy-html5
# channels:
#  - IOOS
#  - pelson
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
    for root, dirs, files in os.walk('output'):
        new_root = os.path.join('output_branch',
                                os.path.normpath(os.path.relpath(root, 'output')))
        for dir in dirs:
            if dir.startswith('.'):
                dirs.remove(dir)
                continue
            new = os.path.join(new_root, dir)
            os.mkdir(new)
        for fname in files:
            if fname.startswith('.'):
                continue
            old = os.path.join(root, fname)
            new = os.path.join(new_root, fname)
            if fname.endswith('.html'):
                print('\nConverting {}:'.format(old))
                cmd = ['tidy5', '-config', 'tidy_config.txt', old]
                with open(new, 'w') as fh:
                    try:
                        code = subprocess.check_call(cmd, stdout=fh)
                    except subprocess.CalledProcessError as err:
                        if err.returncode != 1:
                            raise
            else:
                shutil.copy(old, new)

    for fname in sorted(glob.glob('output/*')):
        continue
        if os.path.isdir(fname):
            shutil.copytree(fname, os.path.join('output_branch', os.path.basename(fname)))
        elif fname.endswith('.html'):
            cmd = ['tidy5', '-config', 'tidy_config.txt', fname]
            with open(os.path.join('output_branch', os.path.basename(fname)), 'w') as fh:
                subprocess.check_call(cmd, stdout=fh)
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
