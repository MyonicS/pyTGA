# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyTGA'
copyright = '2025, Sebastian Rejman'
author = 'Sebastian Rejman'
version = '0.1.0'
release = '0.1.0'


# Configure autodoc
autodoc_member_order = 'bysource'
autoclass_content = 'both'

# For Jupyter notebook support
nbsphinx_execute = 'never'  # Don't re-execute notebooks




# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'myst_parser'
]

# Configure MyST-Parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
]
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

language = 'English'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    # Ensure the logo paths use the full path from static directory
    "light_logo": "logo_v1.svg",
    "dark_logo": "logo_v1_dark.svg",
    "light_css_variables": {
        "color-brand-primary": "#c2389e",
        "color-background-secondary": "#f0fbff",
    },
    "dark_css_variables": {
        "color-brand-primary": "#f4a900",
        "color-background-primary": "#151420",
        "color-background-secondary": "#1a1d25",
        "color-admonition-background": "#190242",
    },
}

# Logo settings are now handled by html_theme_options with light_logo and dark_logo