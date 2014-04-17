# -*- coding: utf-8 -*-

import os, sys
from setuptools import setup

kwargs = {}
if sys.version_info[0] >= 3:
    print('Converting code to Python 3 helped by 2to3')
    kwargs['use_2to3'] = True

install_requires = ["requests"]
tests_require = ["mock"]

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "slumber",
    version = "0.7.1.dev",
    description = "A library that makes consuming a REST API easier and more convenient",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
        open(os.path.join(base_dir, "CHANGELOG.rst"), "r").read()
    ]),
    url = "http://slumber.in/",
    author = "Donald Stufft",
    author_email = "donald.stufft@gmail.com",
    packages = ["slumber"],
    zip_safe = False,
    install_requires = install_requires,
    tests_require = tests_require,
    test_suite = "tests.get_tests",
    **kwargs
)
