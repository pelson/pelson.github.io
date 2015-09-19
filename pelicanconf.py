#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Phil Elson'
SITENAME = u"Phil Elson - Software | Science | Python"
SITEURL = '' #'pelson.github.io'
SITEURL = '//localhost:8080/output/' #'pelson.github.io'
GITHUB_URL = 'http://github.com/pelson/pelson.github.io'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'

# Blogroll
LINKS =  []

# Social widget
SOCIAL = []

DEFAULT_PAGINATION = False

DISQUS_SITENAME = "pelson"
GOOGLE_ANALYTICS = "UA-43268601-1"

OUTPUT_RETENTION = [".git"]
OUTPUT_PATH = "outputasdasd/"

ARTICLE_URL = '{date:%Y}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'

PLUGIN_PATH = '../pelican-plugins'
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook', 'summary',
           'feed_summary']
FEED_USE_SUMMARY = True

THEME = "simple"
THEME =  "pelican_extras/pelson-custom"
