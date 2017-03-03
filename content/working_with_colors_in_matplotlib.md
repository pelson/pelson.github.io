Title: Working with colours in matplotlib
Date: 2013-06-03 12:00
Category: article
Tags: matplotlib, Python
Slug: working_with_colors_in_matplotlib
Author: Phil Elson
is_notebook: 1
gist_url: https://gist.github.com/pelson/5636372
nbviewer_url: http://nbviewer.ipython.org/5636372
summaryimg: thumb.png

When dealing with colours in scientific visualisations some people like to have a colourmap
which can be indexed into to pick specific colours. Whilst this isn't necessarily the best
way of handling colours in matplotlib, it certainly adds a degree of familiarity to users
who have come over from other visualisation tools, such as IDL.

In this article I'll cover one approach to using the colour-by-index paradigm in matplotlib.

<!-- PELICAN_END_SUMMARY -->

{% notebook working_with_colors_in_mpl/working_with_colors.ipynb cells[1:] %}

This article certainly shows a way of handling the colour-by-index paradigm,
though it must be said that handling colours like this in matplotlib is not
necessarily the best approach - I'll leave that to a future article.

Find this useful? How do you handle colours in your matplotlib figures? Is there a
killer feature you think matplotlib is missing out on? Let me know via the comments
section.

