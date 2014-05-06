# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class SlumberBaseException(Exception):
    """
    All Slumber exceptions inherit from this exception.
    """


class SlumberHttpBaseException(SlumberBaseException):
    """
    All Slumber HTTP Exceptions inherit from this exception.
    """

    def __init__(self, response):
        self.response = response
        value = "%s Error %s %s: %s, text: %s" % ('Client' if response.status_code <= 499 else 'Server',
                                                  response.status_code, response.reason, response.url, response.text)
        super(SlumberHttpBaseException, self).__init__(value)


class HttpClientError(SlumberHttpBaseException):
    """
    Called when the server tells us there was a client error (4xx).
    """


class HttpServerError(SlumberHttpBaseException):
    """
    Called when the server tells us there was a server error (5xx).
    """


class SerializerNoAvailable(SlumberBaseException):
    """
    There are no available Serializers.
    """


class SerializerNotAvailable(SlumberBaseException):
    """
    The chosen Serializer is not available.
    """


class ImproperlyConfigured(SlumberBaseException):
    """
    Slumber is somehow improperly configured.
    """
