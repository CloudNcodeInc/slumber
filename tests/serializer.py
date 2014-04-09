# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import slumber
import slumber.serialize


class ResourceTestCase(unittest.TestCase):

    def test_json_get_serializer(self):
        s = slumber.serialize.Serializer()

        for content_type in [
                                "application/json",
                                "application/x-javascript",
                                "text/javascript",
                                "text/x-javascript",
                                "text/x-json",
                            ]:
            s.get_serializer(content_type=content_type)
