Title: Introducing multistage-build: a proxy build-backend with customisable pre- and post-build hooks
Date: 2026-09-22 06:00
Category: article
Tags: Python, packaging, PEP-517
Slug: multistage_build
Author: Phil Elson
is_notebook: 0


Sometimes you want to customise your Python project's build with a pre-processing or post-processing step that isn't built-in to the PEP-517 build backend that you happen to be using. In my day-to-day work I have multiple such needs, including:

 * The ability to run tasks before the actual build takes place, including things like code generation (I have one case where I generate a synchronous module from an equivalent async module, meaning I can maintain a consistent API for both approaches).
 * The ability to inject metadata into a wheel after build (I was investigating the `Requires-External` core metadata).

In the past, you would have used custom commands in `setuptools`/`distutils`. With `pyproject.toml`, build backends choose the functionality they wish to support, but in general there are no standardised hooks that you can reliably use across all backends: a hook that exists for `hatchling` won't help you if you happen to be using `setuptools` or `flit`. Building a whole new build backend just to trigger a simple pre- or post-processing step doesn't make any sense, so you are left with continuing to use `setup.py` alongside `pyproject.toml` - this has its own downsides, and is also coupled tightly to the build backend you are using. This is where `multistage-build` can help.

<!-- PELICAN_END_SUMMARY -->


## multistage-build: a PEP-517 build backend which proxies your real build backend

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

The `my_hooks` module lives in the same directory as `pyproject.toml`. The `hook-path` mechanism is analogous to the PEP-517 backend-path mechanism, and allows code local to our project to be run. It only needs to be a plain Python module:

```python
# my_hooks.py
def add_requires_external(wheel_path):
    # open the wheel, patch its METADATA file, write it back
    ...
```

When pip, uv or build ask the backend to build a wheel, multistage-build delegates to the configured build backend (in this example, setuptools), and then calls `add_requires_external` with the resulting wheel path before returning the result to the build frontend. From the frontend's point of view a normal wheel has been produced; multistage-build just handed the wheel to your hook first.

Pre-hooks also exist, and they run before the real backend is called, receiving the arguments the backend was about to see. This is handy for things like code generation, or anything else that has to happen to the source tree before the real build backend does its thing.

A useful side-effect of this design is that the hook itself is not tied to any particular backend. If you choose to move from setuptools to hatchling, or to some other build backend, you simply change the `[tool.multistage-build]` build-backend line, and the hook stays in place.


## Respecting the PEP-517 contract

Multistage-build only wraps the real backend, and does not enforce any consistency between the hooks you register. That is entirely the responsibility of the hook creator. The most obvious invariant to preserve is metadata consistency - if a `post-build-wheel` hook adds a field to the wheel's `METADATA`, then a frontend that later calls `prepare_metadata_for_build_wheel` on the same project should get the same field back. That means also registering a matching hook on `post-prepare-metadata-for-build-wheel` (and, for editable builds, on `post-prepare-metadata-for-build-editable`), so that whatever a frontend can see up-front lines up with whatever eventually ends up in the wheel.

It is conceivable that another layer, built on top of multistage-build, could manage metadata modifications for you in a standards-compliant way. That is out of scope for the multistage-build backend itself, whose focus is purely on being a simple PEP-517 function proxy.


## Hooks as plugins

There is also an entry-points-based mode, which is closer to a proper plugin system. Rather than declaring a hook in each project's `pyproject.toml`, a helper tool can advertise itself:

```toml
# in the helper tool's own pyproject.toml
[project.entry-points.multistage_build]
post-build-wheel = "my_mod:the_hook"
```

Any project that lists that helper tool in its `[build-system].requires`, and uses `multistage_build:backend`, will then pick up the hook automatically. No additional configuration is required in the consuming project's `pyproject.toml`, and it lets a hook be installable as a build dependency, rather than having to be declared per-project.

As a hypothetical example, a `multistage-mypyc` library could register a `pre-build-wheel` entry point that runs [mypyc](https://mypyc.readthedocs.io/) over the source tree and drops the resulting extension modules where the underlying backend will pick them up. Any project wanting mypyc compilation would then add `multistage-mypyc` as a build requirement, choose `multistage_build:backend`, and get the same behaviour with any of the mainstream backends. [hatch-mypyc](https://github.com/ofek/hatch-mypyc) already does this for hatchling. At the time of writing I am not aware of an equivalent that works across build backends.

One criticism I have of this approach is that it can be a bit opaque as to the build processes that are enabled for a build. Another is that there is no control of the order of these entrypoint registered hooks. I don't yet know if I think this is a deal-breaker, or if the convenience of simply adding a build-time requirement to automatically trigger new behaviour is a price worth paying. I've been playing with this approach a bit, and plan to roll it out to a number of my projects to get a feeling for how it plays out. Feedback welcome!


## Next steps

The build backend is working robustly, and I am very happy with the outcome. I think this unlocks a lot of potential for hooking into the build phase of a project, and I'm using it in multiple places already. If this were to become a popular thing, it is conceivable that this could be a built-in concept in the PEP-517 mechanism, rather than requiring a dedicated proxy backend, but I think that is a long-shot.

I'd be interested to know your thoughts on this - is this against the grain of the PEP-517 spec? Or is this a useful step which gives us more atomic build capabilities and moves us towards looser coupling to specific build backends?

