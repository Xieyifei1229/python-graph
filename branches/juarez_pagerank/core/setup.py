#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup, find_packages
except ImportError as ie:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

# Startup
appname = "python-graph-core"
appversion = "1.7.0"

setup(
        name = appname,
        version = appversion,
        author = "Pedro Matiello",
        namespace_packages = ["pygraph"],
        packages = ["pygraph"] + [ os.path.join("pygraph", a) for a in find_packages("pygraph") ],
        author_email = "pmatiello@gmail.com",
        description = "A library for working with graphs in Python",
        license = "MIT",
        keywords = "python graphs hypergraphs networks library algorithms",
        url = "http://code.google.com/p/python-graph/",
        classifiers = ["License :: OSI Approved :: MIT License","Topic :: Software Development :: Libraries :: Python Modules"],
        long_description = "python-graph is a library for working with graphs in Python. This software provides a suitable data structure for representing graphs and a whole set of important algorithms.",
)
