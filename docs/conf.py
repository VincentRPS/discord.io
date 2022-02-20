# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('extensions'))


# -- Project information -----------------------------------------------------

project = 'discord.io'
copyright = '2021-present, VincentRPS'
author = 'VincentRPS'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.extlinks',
    'exception_hierarchy',
    'resourcelinks',
    'hoverxref.extension',
    # 'sphinx.ext.githubpages', putting this off until we have a domain.
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']


# -- Extension configuration -------------------------------------------------

extlinks = {
    "issue": (f"https://github.com/VincentRPS/discord.io/issues/%s", "#"),
}

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
"""

resource_links = {
    'discord': 'https://discord.gg/cvCAwntVhm',
    'issues': 'https://github.com/VincentRPS/discord.io/issues',
    'discussions': 'https://github.com/VincentRPS/discord.io/discussions',
    'examples': 'https://github.com/VincentRPS/discord.io/tree/master/examples',
}

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'py': ('https://docs.python.org/3', None),
}
