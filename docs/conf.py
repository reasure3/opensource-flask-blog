"""Sphinx configuration for the Flask Study Notes Service."""

from __future__ import annotations

import os
import sys

PROJECT_ROOT = os.path.abspath("..")
sys.path.insert(0, PROJECT_ROOT)

project = "Flask Study Notes Service"
author = "reasure3"
copyright = "2026, reasure3"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "en"

html_theme = "alabaster"
html_title = "Flask Study Notes Service Docs"
html_static_path = ["_static"]

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
