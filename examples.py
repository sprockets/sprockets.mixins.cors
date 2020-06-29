#!/usr/bin/env python

import logging

from tornado import ioloop, web

from sprockets.mixins import cors


class SimpleRequestHandler(cors.CORSMixin, web.RequestHandler):
    """Very simple request handler that CORS enables the GET endpoint."""

    def initialize(self, creds=False, req_headers=None):
        super(SimpleRequestHandler, self).initialize()
        self.cors.allowed_methods.add('GET')
        self.cors.credentials_supported = creds
        if req_headers:
            self.cors.request_headers.update(hdr.lower()
                                             for hdr in req_headers)

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


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-8s %(name)s: %(message)s')
    app = web.Application([
        web.url('/public', SimpleRequestHandler),
        web.url('/private', SimpleRequestHandler, {'creds': True}),
    ], cors_origins=['http://www.example.com'], debug=True)
    app.listen(8000)

    iol = ioloop.IOLoop.instance()
    try:
        iol.start()
    except KeyboardInterrupt:
        logging.info('stopping IOLoop')
        iol.add_callback(iol.stop)
