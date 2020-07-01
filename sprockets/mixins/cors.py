"""

Tornado RequestHandler mix-in for implementing a CORS enabled endpoint.

The CORS_ specification describes a method of securing javascript access
to web resources across access domains.  This module implements a mix-in
to be used with :class:`tornado.web.RequestHandler` that provides much
of the functionality required by CORS_.

.. _CORS: http://www.w3.org/TR/cors/

"""

version_info = (1, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)

SIMPLE_REQUEST_HEADERS = frozenset(('accept', 'accept-language',
                                    'content-language'))
"""
Request headers that get special treatment per CORS.

These are considered "simple headers" and are always acceptable to
send in CORS-enabled requests.

"""


class CORSSettings(object):
    """
    Configures the CORS behavior.

    .. attribute::allowed_methods

       The :class:`set` of CORS accepted HTTP methods.  This controls
       the :mailheader:`Access-Control-Allow-Methods` response header.

    .. attribute::allowed_origins

       The :class:`set` of origins that are allowed for the endpoint.
       This controls the :mailheader:`Access-Control-Allow-Origin`
       response header.  If the requested origin is in this set, then
       the origin is allowed; otherwise, a :http:statuscode:`403` is returned.

    .. attribute::credentials_supported

       Should the mix-in generate the
       :mailheader:`Access-Control-Allow-Credentials` header in the
       response.

    .. attribute::request_headers

       A :class:`set` of header names that are acceptable in cross-origin
       requests.  Headers added to this set **MUST** be lower-cased before
       adding them to the set.

    """
    def __init__(self):
        self.allowed_methods = set()
        self.allowed_origins = set()
        self.credentials_supported = False
        self.request_headers = {header.lower()
                                for header in SIMPLE_REQUEST_HEADERS}


class CORSMixin(object):
    """
    Mix this in over a :class:`tornado.web.RequestHandler` for CORS support.

    .. attribute::cors

       A :class:`.CORSSettings` instance that controls the behavior of
       the mix-in.

    """

    def initialize(self, **kwargs):
        self.cors = CORSSettings()
        self.cors.allowed_origins.update(self.settings.get('cors_origins', []))
        super(CORSMixin, self).initialize(**kwargs)

    def prepare(self):
        super(CORSMixin, self).prepare()
        if not self._finished and self.request.method != 'OPTIONS':
            origin = self.request.headers.get('Origin')
            if origin in self.cors.allowed_origins:
                self.set_header('Access-Control-Allow-Origin', origin)
                if self.cors.credentials_supported:
                    self.set_header('Access-Control-Allow-Credentials', 'true')

    def options(self):
        """
        Respond to an :http:method:OPTIONS request.

        This method relies on :attr:`self.SUPPORTED_METHODS` for the
        content of the :http:header:Allow response header.  The CORS
        specific headers are generated based on the :attr:`.cors`
        attribute.

        """
        self.set_header('Allow', ','.join(self.SUPPORTED_METHODS))
        self.set_status(204)
        if 'Origin' in self.request.headers:
            if self._cors_preflight_checks():
                self._build_preflight_response(self.request.headers['Origin'])
            else:
                self.set_status(403)

    def _cors_preflight_checks(self):
        try:
            origin = self.request.headers['Origin']
            method = self.request.headers['Access-Control-Request-Method']
            headers = self.request.headers.get(
                'Access-Control-Request-Headers', '')
        except KeyError:
            return False

        headers = _filter_headers(headers, self.cors.request_headers)
        return (origin in self.cors.allowed_origins and
                method in self.cors.allowed_methods and
                len(headers) == 0)

    def _build_preflight_response(self, origin):
        self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Methods',
                        ','.join(self.cors.allowed_methods))
        if self.cors.credentials_supported:
            self.set_header('Access-Control-Allow-Credentials', 'true')
        exposed_headers = self.cors.request_headers - SIMPLE_REQUEST_HEADERS
        if exposed_headers:
            self.set_header('Access-Control-Allow-Headers',
                            ','.join(exposed_headers))

    def _clear_headers_for_304(self) -> None:
        # Overrides '_clear_headers_for_304' method from
        # web.RequestHandler to not clear the ALLOW header when the status
        # code is set to 204. This is bug in Tornado, which is fixed in the
        # Tornado v6.1 but not yet released. This method can be removed once
        # it is updated to Tornado v6.1
        headers = [
            'Content-Encoding',
            'Content-Language',
            'Content-Length',
            'Content-MD5',
            'Content-Range',
            'Content-Type',
            'Last-Modified',
        ]
        for h in headers:
            self.clear_header(h)


def _filter_headers(header_str, simple_headers):
    header_str = header_str.lower().replace(' ', '').replace('\t', '')
    if not header_str:
        return set()

    header_set = {str(value) for value in header_str.split(',')}
    header_set.difference_update(simple_headers)
    header_set.difference_update('')
    return header_set
