Title: Converting rasters to SVG, and creating a rudimentary font with font-forge - Part 4 of an XKCD font saga
Date: 2017-04-21
Category: field-notes
Tags: XKCD, fonts, Python
Slug: xkcd_font_raster_to_vector_and_basic_font_creation
Author: Phil Elson

In [part three]({filename}/field_notes/xkcd_font_pt3.md) of my XKCD font saga I generated several hundred glyphs as PPM images, and
classified them with their associated character(s). In this installment, I will convert the raster glyphs into vector form (SVG) and then
generate a rudimentary font using fontforge.

<!-- PELICAN_END_SUMMARY -->

If you'd like to follow along, the input files for this article may be found at [https://gist.github.com/pelson/1d6460289f06acabb650797b88c15ae0](https://gist.github.com/pelson/1d6460289f06acabb650797b88c15ae0),
while the code (in notebook form) and output may be found at [https://gist.github.com/pelson/18434e3bd37dcde8dd28a5a24def0060](https://gist.github.com/pelson/18434e3bd37dcde8dd28a5a24def0060).

I make no apologies for the amount of code here - I've tidied it up a little, but it is representative of the journey I have taken to produce
a fully functional XKCD font. If you just want to see the resulting font you can scroll about three-quaters of the way down the page to 
[play with the final font in your browser](#font-final).


{% notebook ./xkcd_font_svg_and_creation/notebook.ipynb %}
