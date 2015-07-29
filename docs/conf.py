#!/usr/bin/env python
import alabaster

from sprockets.mixins import cors

project = 'sprockets.mixins.cors'
copyright = '2015, AWeber Communication, Inc.'
version = cors.__version__
release = '.'.join(str(v) for v in cors.version_info[0:2])

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain',
]

templates_path = []
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_style = 'custom.css'
html_theme_path = [alabaster.get_path()]
html_static_path = ['static']
html_sidebars = {
    '**': ['about.html', 'navigation.html'],
}
html_theme_options = {
    'github_user': 'sprockets',
    'github_repo': 'sprockets.mixins.cors',
    'description': 'Tornado CORS helper',
    'github_banner': True,
    'travis_button': True,
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'tornado': ('http://www.tornadoweb.org/en/latest/', None),
}
