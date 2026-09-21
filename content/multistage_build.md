Title: Adding pre- and post-build hooks to any Python build backend with multistage-build
Date: 2026-09-21 12:00
Category: article
Tags: Python, packaging, PEP-517
Slug: multistage_build
Author: Phil Elson
is_notebook: 0


## Motivation

Sometimes you need to customise a Python project's build with a pre-processing or post-processing step that isn't entirely standard. In my day-to-day work I have multiple such needs, including:

 * The ability to inject metadata into a wheel after build (I was investigating the `Requires-External` core metadata).
 * The ability to run tasks before the actual build takes place, including things like code generation (for example, generating a synchronous module from an asynchronous one).

In the past, you would have used custom commands in setuptools/distutils. Nowadays, such hooks exist for specific build backends, but not in all cases, and not in a consistent way. Even where a hook mechanism does exist, it is tied to the particular backend, so a hook you have written for hatchling won't help you if you happen to be using setuptools or poetry-core.


<!-- PELICAN_END_SUMMARY -->


## My solution

Inspired by tools such as [setuptools-ext](https://github.com/wimglenn/setuptools-ext), as well as having implemented another specialised build backend in the past, I figured that this could be generalised, and that building a generic multi-stage backend was possible thanks to PEP-517 exposing the backend as ordinary Python functions.

In [multistage-build](https://github.com/pelson/multistage-build) you declare your build backend to be multistage-build, and then configure multistage-build to use another (real) build backend to do the hard build work. However, you can also declare that for particular phases, some other code should be run on either the input for the PEP-517 build hook in question, or the output of the hook. This means that you can, for example, have a post-build job that modifies the wheel before it is returned to whoever called for the build:

```toml
[build-system]
requires = ["multistage-build", "setuptools"]
build-backend = "multistage_build:backend"

[tool.multistage-build]
build-backend = "setuptools.build_meta"
post-build-wheel = [
    {hook-function = "my_hooks:add_requires_external", hook-path = "."},
]

[project]
name = "some-project"
version = "0.1.0"
```

The `my_hooks` module lives in the same directory as `pyproject.toml` (that is what `hook-path = "."` says), and it only needs to be a plain Python module:

```python
# my_hooks.py
def add_requires_external(wheel_path):
    # open the wheel, patch its METADATA file, write it back
    ...
```

When pip, uv or build ask the backend to build a wheel, multistage-build delegates to `setuptools.build_meta.build_wheel` as usual, and then, before returning, calls `add_requires_external` with the resulting wheel path. From the frontend's point of view a normal wheel has been produced; multistage-build just handed the wheel to your hook first.

Pre-hooks are the mirror image: they run before the real backend is called, and receive the arguments the backend was about to see. That is the place to do code generation, or anything else that has to happen to the source tree before setuptools, hatchling or poetry-core has a look at it.

A useful side-effect of this design is that the hook itself is not tied to any particular backend. If you choose to move from setuptools to hatchling, or to some other build backend, you simply change the `[tool.multistage-build]` build-backend line, and the hook stays in place.


## Respecting the PEP-517 contract

Multistage-build only wraps the real backend, and does not enforce any consistency between the hooks you register. That is entirely the responsibility of the hook creator. The most obvious invariant to preserve is metadata consistency: if a `post-build-wheel` hook adds a field to the wheel's `METADATA`, then a frontend that later calls `prepare_metadata_for_build_wheel` on the same project should get the same field back. That means also registering a matching hook on `post-prepare-metadata-for-build-wheel` (and, for editable builds, on `post-prepare-metadata-for-build-editable`), so that whatever a frontend can see up-front lines up with whatever eventually ends up in the wheel.

It is conceivable that another layer, built on top of multistage-build, could manage metadata modifications for you in a standards-compliant way. That is out of scope for the multistage-build backend itself, whose focus is purely on being a simple PEP-517 function proxy.


## Hooks as plugins

There is also an entry-points-based mode, which is closer to a proper plugin system. Rather than declaring a hook in each project's `pyproject.toml`, a helper tool can advertise itself:

```toml
# in the helper tool's own pyproject.toml
[project.entry-points.multistage_build]
post-build-wheel = "my_mod:the_hook"
```

Any project that lists that helper tool in its `[build-system].requires`, and uses `multistage_build:backend`, will then pick up the hook automatically; no additional configuration is required in the consuming project's `pyproject.toml`. Mostly this is how I have used it, because it lets a hook be installable as a build dependency, rather than having to be maintained per project.

As a hypothetical example, a `multistage-mypyc` library could register a `pre-build-wheel` entry point that runs [mypyc](https://mypyc.readthedocs.io/) over the source tree and drops the resulting extension modules where the underlying backend will pick them up. Any project wanting mypyc compilation would then add `multistage-mypyc` as a build requirement, choose `multistage_build:backend`, and get the same behaviour with any of the mainstream backends. [hatch-mypyc](https://github.com/ofek/hatch-mypyc) already does this for hatchling; at the time of writing I am not aware of an equivalent that works across build backends.


## Use cases

I have used this in multiple places in my work projects already. Two categories in particular:

 * Post-build metadata injection. `Requires-External` is a legal wheel metadata field that setuptools does not currently write, but that downstream tooling can consume (with the risk that standardisation in PEP ??? can reasonably add semantics which are incomatible with whatever you do). This is as simple as adding a `post-build-wheel` hook that opens the wheel and adds the field.
 * Pre-build code generation. When the authoritative source of a library is async, and the sync surface is derived from it, running that derivation as a `pre-build-wheel` hook means the generated files never live in the git tree, and an editable install can regenerate them on demand.

Neither of these is a particularly novel use case, but both are the sort of thing that used to live in a bespoke `setup.py` command, and that most modern build backends do not give you an obvious way to do.

If you have use cases of your own, or bug reports, they are welcome at [github.com/pelson/multistage-build](https://github.com/pelson/multistage-build).
