Title: Building a matrix of conda distributions with conda-build-all
Date: 2015-12-09 12:00
Tags: conda
Slug: conda_build_all
Author: Phil Elson
is_notebook: 0
summaryimg: construction.gif

Introducing ``conda-build-all``, a tool which extends ``conda-build`` to provide powerful build
matrix capabilities.

<!-- PELICAN_END_SUMMARY -->

Repositories such as [conda-forge/stages-recipes](https://github.com/ioos/conda-recipes), [SciTools/conda-recipes-scitools](https://github.com/SciTools/conda-recipes-scitools) and [ioos/conda-recipes](https://github.com/ioos/conda-recipes) exist to provide a set of conda recipes, and ultimately, channels from which users can access the product of ``conda-build``-ing those recipes.
The build phase of all of these repositories looks very similar: a tool (ObviousCI) computes the build matrix, builds those distributions which haven't already been built, and then uploads them to their respective channels.
The functionality is tried and tested, and has been powering these repositories for over a year with huge success, however, I recently had need to use this functionality without wanting to upload the built distributions to [conda.anaconda.org](http://conda.anaconda.org) and found the tool didn't *quite* fit the bill.
Additionally, having originally cobbled together ObviousCI with string and sticky-tape to prove the concept of a continuously integrated repo of recipes, I didn't have huge confidence in its ability to function between python/conda/conda-build upgrades.

As a result, I have re-factored the build part of ObviousCI into a general purpose library which can now be used for the original "conda recipe repository" usecase as much as it can for the ad-hoc "just build this" usecase. Critically, the most significant part of this re-factoring was adding a huge array of unit and integration tests which can be used to ensure expected behaviour is unchanged through future dependency version upgrades.

The new CLI is ``conda-build-all`` (BSD license) and is developed at [SciTools/conda-build-all](https://github.com/SciTools/conda-build-all).

### The build matrix

So what does a build matrix actually look like? Let's jump in at the deep-end and look at a package which has a numpy C-API dependency.
Whilst numpy's ABI is (intended to be) [forward-compatible](http://stackoverflow.com/a/18369312/741316), in practice it is safer to compile against a specific version and "pin" the distribution to that version.
Essentially, that means we need to build our recipe N times, where N is the number of numpy versions we wish to support.
Of course, the same is true for Python itself, leading to a permutation problem of up to ``NxM`` builds (N: number of supported numpy versions; M: number of supported Python versions).

The current conda recipe form for such a package looks like:
 
```
package:
    name: my_library
    version: 1.0
requirements:
    build:
        - python
        - numpy x.x
    run:
        - python
        - numpy x.x
```

Whilst I believe there is [room for improvement](https://github.com/conda/conda-build/pull/650) in the recipe definition, it is still pretty easy to define a complex set of build- and run-time dependencies.

With the existing ``conda-build`` tool, should we want to build this for Python 2.7, 3.4 and 3.5, and against numpy 1.9 and 1.10 (the latest versions of these libraries at the time of writing), things can get a little tedious:

```
CONDA_PY=27 CONDA_NPY=19 conda build my_library
CONDA_PY=34 CONDA_NPY=19 conda build my_library
CONDA_PY=35 CONDA_NPY=19 conda build my_library
CONDA_PY=27 CONDA_NPY=110 conda build my_library
CONDA_PY=34 CONDA_NPY=110 conda build my_library
CONDA_PY=35 CONDA_NPY=110 conda build my_library
```

With ``conda-build-all`` the special environment variables are taken care of for you (and importantly there is future scope to generalise beyond Python & numpy) and a build matrix is computed:

```
$ conda-build-all my_library
Resolving distributions from 1 recipes... 
Computed that there are 7 distributions from the 1 recipes:
Resolved dependencies, will be built in the following order: 
    my_library-1.0-np19py26_0 (will be built: True)
    my_library-1.0-np110py27_0 (will be built: True)
    my_library-1.0-np19py27_0 (will be built: True)
    my_library-1.0-np110py34_0 (will be built: True)
    my_library-1.0-np19py34_0 (will be built: True)
    my_library-1.0-np110py35_0 (will be built: True)
    my_library-1.0-np19py35_0 (will be built: True)
```

Notice how this command is not conceptually equivalent to the original ``conda-build`` calls as I have not asked for particular versions to build against.
``conda-build-all`` has chosen the top two major versions and within those, the top two minor versions of the packages which require "pinning". Unfortunately, that included Python 2.6, which I didn't really want - to resolve that, we can add extra conditions to our build:

```
$ conda-build-all my_library --matrix-conditions "python >=2.7"
Fetching package metadata: ........
Resolving distributions from 1 recipes... 
Computed that there are 6 distributions from the 1 recipes:
Resolved dependencies, will be built in the following order: 
    my_library-1.0-np110py27_0 (will be built: True)
    my_library-1.0-np19py27_0 (will be built: True)
    my_library-1.0-np110py34_0 (will be built: True)
    my_library-1.0-np19py34_0 (will be built: True)
    my_library-1.0-np110py35_0 (will be built: True)
    my_library-1.0-np19py35_0 (will be built: True)
```

We now have functionally equivalent behaviour that will move forwards as new Python and numpy versions become available.

### Building multiple recipes in a single call

``conda-build-all`` knows what a conda recipe looks like, and will traverse the directories you give it to look for things to build.

Supposing we have a directory of recipes which we wish to build, such as the following:

```
$ find * -name meta.yaml -exec sh -c "echo RECIPE: {}; cat {}; echo" \;
RECIPE: my_recipes_directory/my_library/meta.yaml
package:
    name: my_library
    version: 1.0
requirements:
    build:
        - python
        - numpy x.x
    run:
        - python
        - numpy x.x

RECIPE: my_recipes_directory/my_other_library/meta.yaml
package:
    name: my_other_library
    version: 1.0
requirements:
    build:
        - python
        - numpy x.x
    run:
        - python
        - numpy x.x
```

We can simply call ``conda-build-all`` on the directory of recipes to have them built appropriately:

```
$ conda-build-all my_recipes_directory --matrix-conditions "python 2.7.*|3.5.*"
Fetching package metadata: ........
Resolving distributions from 2 recipes... 
Computed that there are 8 distributions from the 2 recipes:
Resolved dependencies, will be built in the following order: 
    my_library-1.0-np110py27_0 (will be built: True)
    my_library-1.0-np19py27_0 (will be built: True)
    my_library-1.0-np110py35_0 (will be built: True)
    my_library-1.0-np19py35_0 (will be built: True)
    my_other_library-1.0-np110py27_0 (will be built: True)
    my_other_library-1.0-np19py27_0 (will be built: True)
    my_other_library-1.0-np110py35_0 (will be built: True)
    my_other_library-1.0-np19py35_0 (will be built: True)
```


This functionality becomes invaluable when we wish to build many packages, such is the case for the conda-recipes repositories mentioned earlier.

### Only building the missing distributions

The build matrix is supremely useful, but it does come at the cost of the extra time needed to build the many distributions.
With repositories full of recipes, it is easy to come to hundreds of build matrix items. If we want to be able to run ``conda-build-all`` on a regular basis, we can't reasonably expect to build each of those items each time.
Therefore, ``conda-build-all`` has the ability to inspect various locations to determine if a distribution has already been built.
In fact, the default behaviour is to inspect the local conda-build directory to determine if a distribution has already been built locally.
Other options include the ability to inspect conda channels as well as arbitrary local directories.
Supposing we wanted the ``pelson/channel/testing`` channel to have all of the built distributions from ``my_recipes_directory``, we can use ``conda-build-all`` to good effect:

```
conda-build-all my_recipes_directory/ --matrix-conditions "python 2.7.*|3.5.*" \
    --inspect-channels "pelson/channel/testing" \
    --upload-channels "pelson/channel/testing" \
    --no-inspect-conda-bld-directory
```

### Summary

``conda-build-all`` is a tool which builds on top of ``conda-build`` to give powerful build-matrix options when building conda distributions.
It has come from ``ObviousCI``, whose primary objective was to simplify the build and upload of many recipes in a Continuous Integration environment.
In migrating the codebase from ``ObviousCI`` several new test strategies have been developed - making ``conda-build-all`` easier to maintain, and giving rise to the possibility of improving the ``conda`` and ``conda-build`` test suites themselves.
