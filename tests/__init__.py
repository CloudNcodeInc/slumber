# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os.path, unittest


def get_tests():
    start_dir = os.path.dirname(__file__)
    return unittest.TestLoader().discover(start_dir, pattern="*.py")
