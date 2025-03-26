# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
sys.path.insert(0, '../..')

import system_helpers

project = 'system-helpers'
copyright = '2025, ULiège CSM'
author = 'ULiège CSM'
release = system_helpers.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'autoapi.extension',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# Autodoc configuration
autodoc_default_options = {
    'members'          : True,
    'show-inheritance' : False,
    'undoc-members'    : True,
}

# Intersphinx configuration
intersphinx_mapping = {
    'python' : ('https://docs.python.org/3', None),
}

# nitpick ignore rules
nitpick_ignore = [
    # https://github.com/sphinx-doc/sphinx/issues/13178
    ("py:class", "pathlib.Path"),
    ("py:obj",   "argparse.Action"),
    ("py:class", "argparse.Namespace"),
    ("py:class", "argparse.ArgumentParser"),
    ("py:class", "pytest_console_scripts.ScriptRunner"),
]

# autoapi configuration
autoapi_dirs = [
    '../../system_helpers',
    '../../tests',
]
