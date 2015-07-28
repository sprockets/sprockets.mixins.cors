from tornado import web

from sprockets.mixins import cors


class SimpleRequestHandler(cors.CORSMixin, web.RequestHandler):
    """Very simple request handler that CORS enables the GET endpoint."""

    def initialize(self, creds=False):
        super(SimpleRequestHandler, self).initialize()
        self.cors.allowed_methods.add('GET')
        self.cors.credentials_supported = creds

    def prepare(self):
        # This is used to test that the mixin does not interfere
        # with request failures.  You really shouldn't call super()
        # after you explicitly finish() but anyway...
        if 'X-Fail' in self.request.headers:
            self.set_status(400)
            self.finish()

        super(SimpleRequestHandler, self).prepare()

    def get(self):
        self.set_status(204)
        self.finish()
