Title: Segment, extract, and combine features of an image with SciPy and scikit-image - Part 2 of an XKCD font saga
Date: 2017-03-20
Category: field-notes
Tags: XKCD, fonts, Python
Slug: xkcd_font_merge_then_extract_glyphs
Author: Phil Elson

In [part one]({filename}/field_notes/xkcd_font.md) of XKCD font saga I gave some background on the XKCD handwriting dataset, and took an initial look at image
segmentation in order to extract the individual strokes from the scanned image.
In this instalment, I will apply the technique from part 1, as well as attempting to merge together strokes to form (some of) the glyphs desired.

I'm going to pay particular attention to "dotted" glyphs, such as "i", "j", ";" and "?". I will need to do future work to merge together
non-dotted glyphs such as the two arrows from "≫", as these are indistinguishable from two characters that happen to be close to one another.

<!-- PELICAN_END_SUMMARY -->

If you'd like to follow along, this notebook and the handwriting file may be found at [https://gist.github.com/pelson/b80e3b3ab9edbda9ac4304f742cf292b](https://gist.github.com/pelson/b80e3b3ab9edbda9ac4304f742cf292b).

{% notebook ./xkcd_font_glyph_extract/part2.ipynb %}


## Conclusion

In summary, I first used ``scipy.ndimage.label`` to pick out the individual features of the handwriting image.
I then extracted the labels from the image, before blending together suitably small images (mostly the dots and short+wide strokes)
into slightly larger composite-strokes. This was an effective technique for bringing back together things like the dots on the glyphs
i, j and !, as well as joining together things like =, % and ±.

Inputs, code, and output can all be found at [https://gist.github.com/pelson/b80e3b3ab9edbda9ac4304f742cf292b](https://gist.github.com/pelson/b80e3b3ab9edbda9ac4304f742cf292b). 

*The next article in this series is*: **[Classifying segmented strokes as characters]({filename}/field_notes/xkcd_font_pt3.md)**.
