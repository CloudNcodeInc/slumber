# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import slumber
import sys


class UtilsTestCase(unittest.TestCase):

    def test_url_join_http(self):
        self.assertEqual(slumber.url_join("http://example.com/"), "http://example.com/")
        self.assertEqual(slumber.url_join("http://example.com/", "test"), "http://example.com/test")
        self.assertEqual(slumber.url_join("http://example.com/", "test", "example"), "http://example.com/test/example")

        self.assertEqual(slumber.url_join("http://example.com"), "http://example.com/")
        self.assertEqual(slumber.url_join("http://example.com", "test"), "http://example.com/test")
        self.assertEqual(slumber.url_join("http://example.com", "test", "example"), "http://example.com/test/example")

    def test_url_join_https(self):
        self.assertEqual(slumber.url_join("https://example.com/"), "https://example.com/")
        self.assertEqual(slumber.url_join("https://example.com/", "test"), "https://example.com/test")
        self.assertEqual(slumber.url_join("https://example.com/", "test", "example"), "https://example.com/test/example")

        self.assertEqual(slumber.url_join("https://example.com"), "https://example.com/")
        self.assertEqual(slumber.url_join("https://example.com", "test"), "https://example.com/test")
        self.assertEqual(slumber.url_join("https://example.com", "test", "example"), "https://example.com/test/example")

    def test_url_join_http_port(self):
        self.assertEqual(slumber.url_join("http://example.com:80/"), "http://example.com:80/")
        self.assertEqual(slumber.url_join("http://example.com:80/", "test"), "http://example.com:80/test")
        self.assertEqual(slumber.url_join("http://example.com:80/", "test", "example"), "http://example.com:80/test/example")

    def test_url_join_https_port(self):
        self.assertEqual(slumber.url_join("https://example.com:443/"), "https://example.com:443/")
        self.assertEqual(slumber.url_join("https://example.com:443/", "test"), "https://example.com:443/test")
        self.assertEqual(slumber.url_join("https://example.com:443/", "test", "example"), "https://example.com:443/test/example")

    def test_url_join_path(self):
        self.assertEqual(slumber.url_join("/"), "/")
        self.assertEqual(slumber.url_join("/", "test"), "/test")
        self.assertEqual(slumber.url_join("/", "test", "example"), "/test/example")

        self.assertEqual(slumber.url_join("/path/"), "/path/")
        self.assertEqual(slumber.url_join("/path/", "test"), "/path/test")
        self.assertEqual(slumber.url_join("/path/", "test", "example"), "/path/test/example")

    def test_url_join_trailing_slash(self):
        self.assertEqual(slumber.url_join("http://example.com/", "test/"), "http://example.com/test/")
        self.assertEqual(slumber.url_join("http://example.com/", "test/", "example/"), "http://example.com/test/example/")

    def test_url_join_encoded_unicode(self):
        expected = "http://example.com/tǝst/"

        url = slumber.url_join("http://example.com/", "tǝst/")
        self.assertEqual(url, expected)

        url = slumber.url_join("http://example.com/", "tǝst/".encode('utf8').decode('utf8'))
        self.assertEqual(url, expected)

    @unittest.skipIf(sys.version_info[0] >= 3, "Python 3 does not allow mixing strings and bytes.")
    def test_url_join_decoded_unicode(self):
        url = slumber.url_join("http://example.com/".encode('utf-8'), "tǝst/")
        expected = "http://example.com/tǝst/"
        self.assertEqual(url, expected)
