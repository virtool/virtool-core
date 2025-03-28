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

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "virtool-core"
author = "Ian Boyes, Blake Smith"

# The full version, including alpha/beta/rc tags
release = "0.0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
]

html_theme_options = {"page_width": "1200px", "sidebar_width": "20%"}

html_sidebars = {
    "**": ["globaltoc.html", "relations.html", "sourcelink.html", "searchbox.html"],
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_favicon = "./favicon.ico"
html_theme = "piccolo_theme"
# html_static_path = ["_static"]
# html_css_files = ["custom.css"]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    "virtool": (
        "https://dev.virtool.ca/projects/virtool/en/latest/",
        None,
    ),
    "core": ("https://dev.virtool.ca/projects/virtool-core/en/latest/", None),
    "workflow": (
        "https://dev.virtool.ca/projects/virtool-workflow/en/latest/",
        None,
    ),
}
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
# intersphinx_disabled_reftypes = ["*"]


source_suffix = {".rst": "restructuredtext", ".txt": "markdown", ".md": "markdown"}
