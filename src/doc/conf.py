# -- Path setup --------------------------------------------------------------
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = '2021 Microservices Architecture Study'
copyright = '2021, Joseph Kim <cloudeyes@gmail.com>'
author = 'Joseph Kim'

# -- General configuration ---------------------------------------------------

extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
    'sphinxcontrib.plantuml',
]


#highlight_language = 'none'
html_sourcelink_suffix = ''
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

add_module_names = False
plantuml_output_format = 'svg'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = "sphinx_rtd_theme"

#html_static_path = ['_static']
