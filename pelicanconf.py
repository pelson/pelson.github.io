#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Phil Elson'
SITENAME = u"Phil Elson - Software | Science | Python"
SITEURL = '' #'pelson.github.io'
RELATIVE_URLS = True
GITHUB_URL = 'http://github.com/pelson/pelson.github.io'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'

# Blogroll
LINKS =  []

# Social widget
SOCIAL = []

STATIC_PATHS = ['images', 'favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/theme/favicon.ico': {'path': 'favicon.ico'}
}

DISQUS_SITENAME = "pelson"
GOOGLE_ANALYTICS = "UA-43268601-1"

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

AUTHOR_SAVE_AS = ''
ARTICLE_URL = '{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}/index.html'
NOTEBOOK_OUTPUT = 'images'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

PLUGIN_PATHS = ['extras/pelican-plugins']
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook', 'summary',
           'feed_summary']
FEED_USE_SUMMARY = True

THEME =  "extras/theme"
DIRECT_TEMPLATES = ('index', 'archives', 'sitemap', 'announce', 'articles', 'field_notes', 'hints')
SITEMAP_SAVE_AS = 'sitemap.xml'

ANNOUNCE_SAVE_AS = 'announce/index.html'
ARTICLES_SAVE_AS = 'articles/index.html'
FIELD_NOTES_SAVE_AS = 'field-notes/index.html'
HINTS_SAVE_AS = 'hints-n-tips/index.html'


# Thanks http://stefaanlippens.net/quick-and-easy-tag-cloud-in-pelican.html
import math
JINJA_FILTERS = {
    'count_to_font_size': lambda c: '{p:.1f}%'.format(p=100 + 25 * math.log(c, 2)),
}


# Code highlights. http://stackoverflow.com/a/33843925/741316
#MARKDOWN = ['codehilite(noclasses=True, pygments_style=native)', 'extra']  # enable MD options
