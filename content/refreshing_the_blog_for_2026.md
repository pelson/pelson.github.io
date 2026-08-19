Title: Updating this blog for 2026
Date: 2026-08-18 12:00
Category: article
Slug: refresh-2026
Author: Phil Elson
is_notebook: 0

Since my last post more than seven years ago I have changed job, moved to a different country, and started a family.
My interests have evolved, and my work capacity is also different: less time (kids), but making more of what there is (more experienced, and AI coding assistants helping with prototyping).
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

## What are my goals for refreshing my blog?

I have reached a point in my career where I no longer feel the need to project my successes in the way that my old blog framed it.
This is a liberating (and, I fully acknowledge, privileged) position, and it means I can focus more on the fun
that I have with technology, rather than always having to aspire to a level that was on-brand.

First and foremost, I want this blog to be a place where I can share ideas and prototypes on all topics that interest me.
In the past I had gathered my writing into `Announcements`, `Field notes`, `Articles` and `Hints & Tips`.
I want to simplify this, perhaps keeping a distinction between "stuff that I wrote and want to share
with my readers" and "stuff that I found useful for myself, and might want to reference it again in the future".

## Where I am now

Since 2019, I have been leading the introduction of Python for accelerator control at CERN.
There was already Python in use before I arrived, but it was mostly ad-hoc and inconsistent.
I formalised the support and designed much of the core infrastructure and controls-system
libraries that many of the high-level controls applications used in operations now rely upon.

Delivering technical solutions in a scientific domain, and building communities around them,
has always featured heavily in my career. CERN is a perfect fit for me, and I love the combination of working with a broad range
of people who use and appreciate the tools I provide, on genuinely exciting scientific endeavours.

Day to day, I write less numeric/scientific code than I used to, and spend more time enabling
others (physicists, operators, hardware experts) to use Python effectively. Beyond the usual
data analysis infrastructure, the primary use of Python is for PyQt-based operational
applications in the CERN control room.

Technology wise there is a lot going on, but at a high level it breaks down into two groups.

Core Python infrastructure:

 * CPython distributions that are the basis for long-term operational use. The accelerator
   schedule drives us to maintain Python versions for the duration of a ~5 year
   run, and in 2026 we have Python versions ranging from 3.7 through to 3.14.
 * A Python package repository (released under the [simple-repository](https://github.com/simple-repository/)
   GitHub org) that works inside an internet-less operational network.
 * Tooling for deploying applications so that they run robustly in the control room.

Controls-system libraries:

 * Talking to lower-level services, and to networked hardware devices, with extensive
   use of asyncio and an increased reliance on typing and static analysis.
 * Bridging Python to Java: JPype for in-house APIs, Py4J for the Spark stack.
 * Bridging Python to C++ via PyBind11.
 * REST client libraries for the higher-level controls services.

Increasingly Python is being seen as the primary user-facing high-level controls language.
As of today, there is no operational support for server-side Python, though there is
already a fair amount of FastAPI (and even some Flask) in use. Over time, I assume this will
grow, and formal support would follow. A clear trend is towards web dashboards backed by
data served via FastAPI, though I don't see more comprehensive applications moving from PyQt
to web in the near future.

## Outside of work

Away from work I have been doing home automation and small hardware projects for many years
now, mostly around home-assistant and ESP8266/ESP32. Whilst the scale and the needs are quite
different, there are some interesting echoes between that world and my professional one that
I like to draw on.

## AI coding assistants

Finally, the arrival of AI coding assistants (Claude in particular) has been genuinely exciting
and a game-changer for me.
It opens up ideas that previously were not viable, simply because of the up-front investment
they would have needed. I have always been a prototype-making sort of person, and AI supports
that mode of working very well.
There are some interesting social challenges around AI usage, but I think _not_ using AI is hard to
justify in 2026. Finding finding the sweet spot between AI and
human effort is something we are all still figuring out.
For prototypes, I think vibe coding works out quite well, but for real code that you want to maintain,
I don't believe that fully automated agentic use of AI produces a satisfactory outcome, neither in
terms of quality, nor in human understanding.

In the same vein, I will use AI to help me author this blog, but always in a collaborative
(human + AI) manner, so that the posts here remain production-quality with me taking full ownership
of what is written.

## What's next

Thus, with the slightly adapted scope and focus, and a long-overdue personal update off my chest, I
hope that this refresh produces some insightful articles that can be enjoyed by readers old and new,
and I look forward to sharing the long list of ideas that I have on the backlog.
