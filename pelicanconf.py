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

ARTICLE_URL = '{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}/index.html'
NOTEBOOK_OUTPUT = 'images'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

PLUGIN_PATH = 'extras/pelican-plugins'
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook', 'summary',
           'feed_summary']
FEED_USE_SUMMARY = True

THEME =  "extras/theme"
DIRECT_TEMPLATES = ('index', 'tags', 'archives', 'sitemap')
SITEMAP_SAVE_AS = 'sitemap.xml'

