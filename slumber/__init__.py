# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import posixpath, urlparse, requests

from . import exceptions
from .serialize import Serializer

__all__ = ["Resource", "API"]


def url_join(base, *args):
    """
    Helper function to join an arbitrary number of URL segments together.
    """
    scheme, netloc, path, query, fragment = urlparse.urlsplit(base)
    path = path if len(path) else "/"
    path = posixpath.join(path, *[('%s' % x) for x in args])
    return urlparse.urlunsplit([scheme, netloc, path, query, fragment])


class ResourceAttributesMixin(object):
    """
    A mixin that makes it so that accessing an undefined attribute on a class
    results in returning a Resource instance. This instance can then be used
    to make calls to the a Resource.
    """

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)
        kwargs = self._store.copy()
        kwargs["base_url"] = url_join(self._store["base_url"], item)
        return self._get_resource(**kwargs)

    def _get_resource(self, **kwargs):
        return self.__class__(**kwargs)


class Resource(ResourceAttributesMixin, object):
    """
    Resource provides the main functionality behind slumber. It handles the
    attribute -> URL, kwargs -> query parameters, and other related behind the
    scenes python to HTTP transformations. It's goal is to represent a single
    resource which may or may not have children.
    """

    def __init__(self, **kwargs):
        self._store = kwargs

    def __call__(self, id=None, format=None, url_override=None):
        """
        Returns a new instance of self modified by one or more of the available
        parameters. These allows us to do things like override format for a
        specific request, and enables the api.resource(ID).get() syntax to get
        a specific resource by it's ID.
        """

        # Short Circuit out if the call is empty
        if id is None and format is None and url_override is None:
            return self

        kwargs = self._store.copy()

        if id is not None:
            kwargs["base_url"] = url_join(self._store["base_url"], id)

        if format is not None:
            kwargs["format"] = format

        if url_override is not None:
            # @@@ This is hacky and we should probably figure out a better way
            #    of handling the case when a POST/PUT doesn't return an object
            #    but a Location to an object that we need to GET.
            kwargs["base_url"] = url_override

        return self.__class__(**kwargs)

    def _request(self, method, data=None, files=None, params=None):
        s = self._store["serializer"]
        url = self._store["base_url"]

        if self._store["append_slash"] and not url.endswith("/"):
            url = url + "/"

        headers = {"accept": s.get_content_type()}

        if self._store.get("token", None):
            headers["Authorization"] = "{token_type} {access_token}".format(**self._store["token"])

        if not files:
            headers["content-type"] = s.get_content_type()
            if data is not None:
                data = s.dumps(data)

        response = self._store["session"].request(method, url, data=data, params=params, files=files, headers=headers)

        if 400 <= response.status_code <= 499:
            raise exceptions.HttpClientError(response)
        elif 500 <= response.status_code <= 599:
            raise exceptions.HttpServerError(response)

        self._ = response
        return response

    def _handle_redirect(self, response, **kwargs):
        # @@@ Hacky, see description in __call__
        resource_obj = self(url_override=response.headers["location"])
        return resource_obj.get(params=kwargs)

    def _try_to_serialize_response(self, response):
        s = self._store["serializer"]

        if response.headers.get("content-type", None):
            content_type = response.headers.get("content-type").split(";")[0].strip()
            try:
                stype = s.get_serializer(content_type=content_type)
                response_content = stype.loads(response.content)
            except exceptions.SerializerNotAvailable:
                response_content = response.content
        else:
            response_content = response.content
        hook = self._store.get("response_hook")
        return hook(self, response_content) if hook else response_content

    def get(self, **kwargs):
        response = self._request("GET", params=kwargs)
        if 200 <= response.status_code <= 299:
            return self._try_to_serialize_response(response)
        else:
            return  # @@@ We should probably do some sort of error here? (Is this even possible?)

    def post(self, data=None, files=None, **kwargs):
        response = self._request("POST", data=data, files=files, params=kwargs)
        if 200 <= response.status_code <= 299:
            return self._try_to_serialize_response(response)
        else:
            # @@@ Need to be Some sort of Error Here or Something
            return

    def patch(self, data=None, files=None, **kwargs):
        response = self._request("PATCH", data=data, files=files, params=kwargs)
        if 200 <= response.status_code <= 299:
            return self._try_to_serialize_response(response)
        else:
            # @@@ Need to be Some sort of Error Here or Something
            return

    def put(self, data=None, files=None, **kwargs):
        response = self._request("PUT", data=data, files=files, params=kwargs)
        if 200 <= response.status_code <= 299:
            return self._try_to_serialize_response(response)
        else:
            return False

    def delete(self, **kwargs):
        response = self._request("DELETE", params=kwargs)
        if 200 <= response.status_code <= 299:
            if response.status_code == 204:
                return True
            else:
                return True  # @@@ Should this really be True?
        else:
            return False


class API(ResourceAttributesMixin, object):

    resource_class = Resource

    def __init__(self, base_url=None, auth=None, format=None, append_slash=True, session=None, serializer=None,
                 token=None, response_hook=None):
        if serializer is None:
            serializer = Serializer(default=format)

        if session is None:
            session = requests.session()
            session.auth = auth

        self._store = {
            "base_url": base_url,
            "format": "json" if format is None else format,
            "append_slash": append_slash,
            "session": session,
            "serializer": serializer,
            "token": token,
            "response_hook": response_hook
        }

        # Do some Checks for Required Values
        if self._store.get("base_url") is None:
            raise exceptions.ImproperlyConfigured("base_url is required")

    def _get_resource(self, **kwargs):
        return self.resource_class(**kwargs)
