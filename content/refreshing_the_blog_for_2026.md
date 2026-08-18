Title: Updating this blog for 2026
Date: 2026-08-18 12:00
Category: article
Slug: refresh-2026
Author: Phil Elson
is_notebook: 0

Since my last post over 7 years ago I have changed job, moved to a different country, and started a family. 
My interests have evolved, and my work capacity is also different with less actual time (kids), yet more efficient with that time (more experienced, and AI coding assistants helping with prototyping).
What hasn't changed over those years is the spark for new ideas which push forward my personal and professional interests,
as well as my desire to share those ideas (normally in the form of prototypes).

I have a backlog of things that I have been
meaning to get around to writing about, and so I intend to bring this blog back to life and reframe it a little to
reflect my current reality.

<!-- PELICAN_END_SUMMARY -->

## The pre-2026 scope of this blog

Before refreshing this blog in 2026, I had the following blurb on the main page:

> As a scientific technical lead at a leading natural sciences research
> institute, I'm fortunate to contribute to a body of tools that empower
> researchers and data scientists across a broad spectrum of fields.
>
> I'm driven by the idea that the modern scientific method is now almost
> entirely dependent upon software, and that, in order to facilitate
> transparency and reproducibility of results, scientific software must
> increasingly become open source.
>
> As well as deep knowledge of the rapidly changing technology landscape,
> development of useful scientific tools depends upon a solid understanding
> of the underlying scientific problem space. For these reasons you will
> find these pages cover the broad spectrum of topics from technology
> through to scientific.

Today, even though I still believe in what I wrote, I find it a bit highbrow and lofty,
especially for a blog where I just want to share ideas and prototypes.

I have been fortunate to have been involved in the early days of maturing
the scientific Python stack, which has
ultimately gone on to change the world (for science, and eventually for AI).
I'm proud of this contribution, including maintaining core tooling and creating a number of
impactful projects of my own. This latter success I attribute to a combination of
hard-work, and my message being in the right place at the right time.

Some of the highlights for me from this epoch include:

 * Having played a leading role in shaping matplotlib, helping it mature into a v1, and become a
   de-facto visualisation library
 * Creating cartopy, a library that extended matplotlib to create geospatial visualisations,
   particularly focussed towards issues such as dateline wraparound (a significant problem
   for atmospheric and oceanographic studies using global modelling)
 * Co-authoring a domain-specific data model library, `Iris`, providing powerful analysis
   and visualisation of NWP (Numerical Weather Prediction) model data. This was created around the
   time that pandas was first released, and was a pre-cursor and direct influence to tools such as
   xarray and dask (which are both awesome libraries!).
 * Building conda-forge, which was a collaborative project from day one, and which still plays an
   important role in providing binary distributions for the Scientific Python stack.
   

## What are my goals for refreshing my blog?

I have reached a point in my career where I no longer feel the need to project my successes in the way that my old blog framed it.
This is a liberating (and, I fully acknowledge, privileged) position, and it means I can focus more on the fun that I have with technology, rather than always having to aspire to a level that was on-brand.

First and foremost, I want this blog to be a place where I can share ideas and prototypes on all topics that interest me.
In the past I had gathered my writing into `Announcements`, `Field notes`, `Articles` and `Hints & Tips`.
I want to simplify this, perhaps keeping a distinction between "stuff that I wrote and want to share
with my readers" and "stuff that I found useful for myself, and might want to reference it again in the future".


- What that scope produced:  conda-execute, notebooks

## 3. Where I am now

- At CERN since 2019, supporting Python for accelerator controls
- Formalised the support; designed core infra and controls-system libs the high-level stack depends on
- Enjoyment of working at CERN; communities and working with others as the driver
- Founding member of the CERN Open Source Program Office (OSPO); wanting to facilitate open source at CERN

## 4. What the work actually looks like now

- Less scientific code, more enabling others (physicists, operators, hardware experts)
- Very little personal Jupyter notebook use these days
- Python distributions
- Package repo for an internet-less networked operations environment
- Core libs bridging Python to C++ (pybind), JVM (JPype), REST
- Visible face: PyQt apps in the control room (long tradition), plus FastAPI data-serving for other tools / web frontends
- Where it is heading: more visualisation, general-purpose controls apps (device-data navigator, timing-system coordinator/config)

## 5. Personal / outside work

- Home automation, ESP8266/ESP32 hardware projects
- Not done at CERN (no ESPs there), and not hardware dev professionally
- But echoes the professional work

## 6. AI coding assistants

- Advent of AI coding assistants (Claude in particular) has been exciting
- Opens up ideas that were not previously viable because of the investment they would require
- Long-time prototype-making type of person; AI supports this well
- Much less convinced about it for operational / critical library code today, IMO

## 7. What this means for the blog

- Widen scope beyond "scientific software"
- Less focus on stuff I intend to support/maintain
- Redesign of the site itself is the next post
