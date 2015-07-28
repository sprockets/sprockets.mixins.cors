"""
Tornado RequestHandler mix-in for implementing a CORS enabled endpoint.
"""

version_info = (0, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)


class CORSSettings(object):
    """
    Configures the CORS behavior.

    .. attribute:: allowed_methods

       The :class:`set` of CORS accepted HTTP methods.  This controls
       the :mailheader:`Access-Control-Allow-Methods` response header.

    .. attribute:: allowed_origins

       The :class:`set` of origins that are allowed for the endpoint.
       This controls the :mailheader:`Access-Control-Allow-Origin`
       response header.  If the requested origin is in this set, then
       the origin is allowed; otherwise, a :http:statuscode:`403` is returned.

    .. attribute:: credentials_supported

       Should the mix-in generate the
       :mailheader:`Access-Control-Allow-Credentials` header in the
       response.

    """
    def __init__(self):
        self.allowed_methods = set()
        self.allowed_origins = set()
        self.credentials_supported = False


class CORSMixin(object):
    """
    Mix this in over a :class:`tornado.web.RequestHandler` for CORS support.

    .. attribute:: cors

       A :class:`.CORSSettings` instance that controls the behavior of
       the mix-in.

    """

    def initialize(self, **kwargs):
        self.cors = CORSSettings()
        self.cors.allowed_origins.update(self.settings.get('cors_origins', []))
        super(CORSMixin, self).initialize(**kwargs)

    def prepare(self):
        super(CORSMixin, self).prepare()
        if not self._finished:
            origin = self.request.headers.get('Origin')
            if origin in self.cors.allowed_origins:
                self.set_header('Access-Control-Allow-Origin', origin)
                if self.cors.credentials_supported:
                    self.set_header('Access-Control-Allow-Credentials', 'true')

    def options(self):
        """
        Respond to an :http:method:`OPTIONS` request.

        This method relies on :attr:`self.SUPPORTED_METHODS` for the
        content of the :http:header:`Allow` response header.  The CORS
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
        self.finish()

    def _cors_preflight_checks(self):
        try:
            origin = self.request.headers['Origin']
            method = self.request.headers['Access-Control-Request-Method']
        except KeyError:
            return False

        return (origin in self.cors.allowed_origins and
                method in self.cors.allowed_methods)

    def _build_preflight_response(self, origin):
        self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Methods',
                        ','.join(self.cors.allowed_methods))
        if self.cors.credentials_supported:
            self.set_header('Access-Control-Allow-Credentials', 'true')
