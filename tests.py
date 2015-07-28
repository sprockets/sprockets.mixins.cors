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
