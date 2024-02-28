# -*- coding: utf-8 -*-

import os
import re
import sys

sys.path.insert(0, os.path.abspath('_ext'))

# -- General configuration ------------------------------------------------
needs_sphinx = '5.3'
extensions = ['cps', 'autosectionlabel']

source_suffix = '.rst'
exclude_patterns = ['AUTHORS.rst', 'THANKS.rst']

master_doc = 'index'

# General information about the project.
project = u'Common Package Specification'
copyright = u'2023, Matthew Woehlke'

release = '.'.join(map(str, [0, 9, 0]))
version = re.match(r'\d+\.\d+', release).group(0)

language = 'en'
primary_domain = 'cps'
#default_role = None

highlight_language = 'none'
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------
html_style = 'cps.css'
html_theme = 'default'

html_theme_options = {
    'footerbgcolor':    '#00182d',
    'footertextcolor':  '#ffffff',
    'sidebarbgcolor':   '#e4ece8',
    'sidebarbtncolor':  '#00a94f',
    'sidebartextcolor': '#333333',
    'sidebarlinkcolor': '#00a94f',
    'relbarbgcolor':    '#00529b',
    'relbartextcolor':  '#ffffff',
    'relbarlinkcolor':  '#ffffff',
    'bgcolor':          '#ffffff',
    'textcolor':        '#444444',
    'headbgcolor':      '#f2f2f2',
    'headtextcolor':    '#003564',
    'headlinkcolor':    '#3d8ff2',
    'linkcolor':        '#2b63a8',
    'visitedlinkcolor': '#2b63a8',
    'codebgcolor':      '#eeeeee',
    'codetextcolor':    '#333333',
    'bodyfont':         "'Noto Sans', sans-serif",
    'headfont':         "'Noto Sans', sans-serif",
}

html_title = f'{project} v{release}'
html_favicon = '_static/cps-favicon.ico'

html_static_path = ['_static']

html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html'
    ]
}

html_domain_indices = False
