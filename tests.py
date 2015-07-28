from __future__ import absolute_import

import unittest

from tornado import testing, web

from examples import SimpleRequestHandler


class OptionSupportTests(testing.AsyncHTTPTestCase):

    def get_app(self):
        return web.Application([web.url('/', SimpleRequestHandler)])

    def test_that_options_is_supported(self):
        response = self.fetch('/', method='OPTIONS')
        self.assertIn(response.code, range(200, 300))

    def test_that_options_includes_supported_methods(self):
        response = self.fetch('/', method='OPTIONS')
        self.assertEqual(response.headers['Allow'],
                         ','.join(SimpleRequestHandler.SUPPORTED_METHODS))


class PreflightTests(testing.AsyncHTTPTestCase):

    def get_app(self):
        return web.Application(
            [web.url('/', SimpleRequestHandler)],
            cors_origins=['http://host.example.com'],
        )

    def test_that_options_understands_origin_header(self):
        response = self.fetch('/', method='OPTIONS',
                              headers={'Origin': 'http://host.example.com',
                                       'Access-Control-Request-Method': 'GET'})
        self.assertIn(response.code, range(200, 300))
        self.assertEqual(response.headers['Access-Control-Allow-Origin'],
                         'http://host.example.com')

    def test_that_preflight_fails_for_unacceptable_origin(self):
        response = self.fetch('/', method='OPTIONS',
                              headers={'Origin': 'https://host.example.com',
                                       'Access-Control-Request-Method': 'GET'})
        self.assertEqual(response.code, 403)

    def test_that_preflight_fails_for_unacceptable_method(self):
        response = self.fetch(
            '/', method='OPTIONS',
            headers={'Origin': 'http://host.example.com',
                     'Access-Control-Request-Method': 'POST'})
        self.assertEqual(response.code, 403)

    def test_that_preflight_fails_when_missing_request_method(self):
        response = self.fetch('/', method='OPTIONS',
                              headers={'Origin': 'http://host.example.com'})
        self.assertEqual(response.code, 403)
