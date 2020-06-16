from __future__ import absolute_import

from examples import SimpleRequestHandler
from tornado import testing, web

from sprockets.mixins import cors


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
            [web.url('/', SimpleRequestHandler),
             web.url('/private', SimpleRequestHandler, {'creds': True}),
             web.url('/reqheader', SimpleRequestHandler,
                     {'req_headers': ['Correlation-ID']})],
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

    def test_that_preflight_generates_allow_credentials_appropriately(self):
        response = self.fetch('/private', method='OPTIONS',
                              headers={'Origin': 'http://host.example.com',
                                       'Access-Control-Request-Method': 'GET'})
        self.assertEqual(response.headers['Access-Control-Allow-Credentials'],
                         'true')

    def test_that_preflight_fails_for_unsupported_request_header(self):
        response = self.fetch('/', method='OPTIONS', headers={
            'Origin': 'http://host.example.com',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Correlation-ID',
        })
        self.assertEqual(response.code, 403)

    def test_that_preflight_succeeds_for_simple_request_headers(self):
        request_headers = ', '.join(s.title()
                                    for s in cors.SIMPLE_REQUEST_HEADERS)
        response = self.fetch('/', method='OPTIONS', headers={
            'Origin': 'http://host.example.com',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': request_headers,
        })
        self.assertIn(response.code, range(200, 300))

    def test_that_preflight_does_not_advertise_simple_request_headers(self):
        request_headers = ', '.join(s.title()
                                    for s in cors.SIMPLE_REQUEST_HEADERS)
        response = self.fetch('/', method='OPTIONS', headers={
            'Origin': 'http://host.example.com',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': request_headers,
        })
        self.assertIn(response.code, range(200, 300))
        self.assertNotIn('Access-Control-Allow-Headers', response.headers)

    def test_that_preflight_advertises_custom_request_headers(self):
        response = self.fetch('/reqheader', method='OPTIONS', headers={
            'Origin': 'http://host.example.com',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Correlation-ID',
        })
        self.assertIn(response.code, range(200, 300))
        self.assertIn('correlation-id',
                      response.headers['Access-Control-Allow-Headers'].lower())


class StandardRequestTests(testing.AsyncHTTPTestCase):

    def get_app(self):
        return web.Application(
            [web.url('/', SimpleRequestHandler),
             web.url('/private', SimpleRequestHandler, {'creds': True})],
            cors_origins=['http://host.example.com'],
        )

    def test_that_get_response_includes_allow_origin(self):
        response = self.fetch('/', headers={
            'Origin': 'http://host.example.com'})
        self.assertEqual(response.headers['Access-Control-Allow-Origin'],
                         'http://host.example.com')

    def test_that_get_response_includes_allow_creds_when_secure(self):
        response = self.fetch('/private', headers={
            'Origin': 'http://host.example.com'})
        self.assertEqual(response.headers['Access-Control-Allow-Origin'],
                         'http://host.example.com')
        self.assertEqual(response.headers['Access-Control-Allow-Credentials'],
                         'true')

    def test_that_get_skips_allow_origin_on_missing_origin_header(self):
        response = self.fetch('/')
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)

    def test_that_get_skips_allow_origin_when_handler_finishes(self):
        response = self.fetch('/', headers={
            'Origin': 'http://host.example.com', 'X-Fail': 'yes please'})
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)
