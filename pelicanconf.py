#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Phil Elson'
SITENAME = u"The gallimaufry of a scientific techie"
SITEURL = ''

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  []

# Social widget
SOCIAL = []

DEFAULT_PAGINATION = False

DISQUS_SITENAME = "pelson"
GOOGLE_ANALYTICS = "UA-43268601-1"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATH = '../pelican-plugins'
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook', 'summary']

THEME = 'pelson-notmyidea-cms'
