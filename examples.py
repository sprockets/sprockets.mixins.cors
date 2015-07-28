from tornado import web

from sprockets.mixins import cors


class SimpleRequestHandler(cors.CORSMixin, web.RequestHandler):
    """Very simple request handler that CORS enables the GET endpoint."""

    def initialize(self, creds=False):
        super(SimpleRequestHandler, self).initialize()
        self.cors.allowed_methods.add('GET')
        self.cors.credentials_supported = creds
