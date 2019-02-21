Title: Running scripts in temporary conda environments with conda execute
Date: 2015-10-03 12:00
Category: announce
Tags: Python, conda
Slug: conda_execute
Author: Phil Elson
is_notebook: 0

Conda is awesome - it is a simple package manager which allows me to create isolated software environments
much like virtualenv. Unlike virtualenv though it can handle any package type, not just python ones.

The more I use it, the more I want to make use of conda's dependency tracking for my own simple scripts to
ensure they were being executed in a suitable environment with the expected dependencies already installed.

``conda build`` is an excellent tool for building your own distributions and sharing them on anaconda.org,
but creating a distribution is tiresome if all you have is a single script, rather than a fully-fledged
software package. That is where ``conda execute`` comes in.


<!-- PELICAN_END_SUMMARY -->


``conda execute`` allows you to run a script of any kind in a temporary environment defined by metadata in the script itself.

For example, take the following Python script:

```
#!/usr/bin/env python

import numpy as np

print(np.random.poisson(size=5))
```

By adding appropriate ``conda execute`` metadata to our script, we can describe the kind of environment
we would need to be able to run this code:

```
$ cat my_script.py

#!/usr/bin/env python

# conda execute
# env:
#  - python >=3
#  - numpy

import numpy as np

print(np.random.poisson(size=5))
```

``conda execute`` can now be used to run this script:

```
$ conda execute -v my_script.py

Using specification: 
env: [python >=3, numpy]
run_with: [/usr/bin/env, python]

Prefix: /Users/pelson/miniconda/tmp_envs/ea977067a8fbeb21a594

[1 2 0 1 0]

```

As you can see, the special comment in the script has been read, and an appropriate temporary environment has been created.

## Temporary environments

In order to provision suitable environments for the executed scripts, ``conda-execute`` implements a temporary environment concept.
Rather than adding a new environment in your conda environments directory (and thus filling up the available environments listed in ``conda env list``), a new "tmp_envs" environments directory has been created, within which ``conda-execute``'s temporary environments are created (this location is configurable with the ``conda-execute/env-dir`` conda config item).
As you may have noticed in the previous example, where the environment created was named ``ea977067a8fbeb21a594``, these temporary environments are named by a hashing algorithm (SHA 256, truncated to 20 characters).
The hash is taken from the ``conda-execute`` metadata of your script, which means that you can re-run a script many times and only need one environment to be created. Additionally, it has the advantage that multiple scripts can share the same environment if their ``conda-execute`` metadata is the same.

Each time a temporary environment is run with ``conda-execute`` a log entry is added, allowing it to keep track of which environments are still in use. Once an environment has been unused for 25 hours any subsequent ``conda-execute`` call will trigger it to be garbage collected, thus preventing your disk filling up with unneeded temporary environments.

## Configurability

``conda-execute`` builds on top of ``conda``'s configuration to allow some customisation in behaviour.
The following ``condarc`` shows the configuration options that are available:

```
conda-execute:
    # The directory to use to hold the temporary environments.
    env-dir: "{config.envs_dirs[0]}/../tmp_envs"

    # The number of hours that an environment should be unused for to be
    # considered for garbage collection.
    remove-if-unused-for: 25
```

## Reproducibility of scripts with ``conda-execute``

There are a few really interesting use-cases which I'm keen to explore with ``conda-execute``.

I'm already making use of ``conda-execute`` as a form of Makefile for this blog. My [make.py](https://github.com/pelson/pelson.github.io/blob/source/make.py) is simply a command line wrapper to the appropriate ``pelican`` sub-command:

```
$> ./make.py --help
usage: Help [-h] {html,publish,reload} ...

positional arguments:
  {html,publish,reload}
    html                Make the html
    publish             Make publishable html, and put it in the
                        output_branch.
    reload              Make the html, and watch the folder for any changes.

optional arguments:
  -h, --help            show this help message and exit
```

The concept of creating reproducible scripts goes far wider than trivial Makefiles though - with ``conda-execute``, because the metadata in the script **is** the definition of the execution environment, important information about its dependencies and how it is run are all embedded into the script itself.

I'm particularly keen to explore the reproducibility angle that ``conda-execute`` brings, particularly for scientific applications.

``conda-execute`` can be found at [github.com/pelson/conda-execute](https://github.com/pelson/conda-execute), and installed with ``conda install conda-execute --channel conda-forge``.

