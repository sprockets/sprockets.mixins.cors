from tornado import web

from sprockets.mixins import cors


class SimpleRequestHandler(cors.CORSMixin, web.RequestHandler):

    pass
