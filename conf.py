# -*- coding: utf-8 -*-

# -- General configuration ------------------------------------------------
needs_sphinx = '6.2'
extensions = ['cps', 'autosectionlabel']

source_suffix = '.rst'
exclude_patterns = ['AUTHORS.rst', 'THANKS.rst']

master_doc = 'index'

# General information about the project.
project = 'Common Package Specification'
copyright = '2024, Matthew Woehlke'

version_info = (0, 12, 0)
release = '.'.join(map(str, version_info))
version = '.'.join(map(str, version_info[:2]))

language = 'en'
primary_domain = 'cps'
# default_role = None

highlight_language = 'json'
pygments_style = 'cps.pygments_styles.CpsDataStyle'

# -- Options for JSON schema output ---------------------------------------
schema_filename = 'cps.schema.json'
schema_root_object = 'package'
schema_id = 'https://cps-org.github.io/cps/' + schema_filename
schema_indent = 2

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
