from tornado import web

from sprockets.mixins import cors


class SimpleRequestHandler(cors.CORSMixin, web.RequestHandler):
    """Very simple request handler that CORS enables the GET endpoint."""

    def initialize(self):
        super(SimpleRequestHandler, self).initialize()
        self.cors.allowed_methods.add('GET')
