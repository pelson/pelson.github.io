Title: Dealing with arrays which are bigger than memory - an introduction to biggus
Date: 2013-09-25 12:00
Category: article
Tags: matplotlib, Python, biggus, voluminous data
Slug: massive_virtual_arrays_with_biggus
Author: Phil Elson
is_notebook: 1
gist_url: https://gist.github.com/pelson/6139282
nbviewer_url: http://nbviewer.ipython.org/6139282
summaryimg: thumb.png

<!-- notice -->
!!! update "Update, August 2026"
    Biggus is no longer developed. For lazy, chunked, out-of-core array
    computation in Python today, use [Dask](https://www.dask.org/). Biggus
    was one of several early efforts in this space and had some influence
    on Dask's design. The rest of this article is preserved unchanged for
    historical interest.
<!-- /notice -->

{% notebook massive_virtual_arrays_with_biggus/massive_arrays_with_biggus.ipynb cells[:1] %}

<!-- PELICAN_END_SUMMARY -->

{% notebook massive_virtual_arrays_with_biggus/massive_arrays_with_biggus.ipynb cells[1:] %}
