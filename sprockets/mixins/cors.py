"""
Tornado RequestHandler mix-in for implementing a CORS enabled endpoint.
"""

version_info = (0, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)


class CORSMixin(object):
    """
    Mix this in over a :class:`tornado.web.RequestHandler` for CORS support.
    """

    def options(self):
        """
        Respond to an :http:method:`OPTIONS` request.

        This method relies on :attr:`self.SUPPORTED_METHODS` for the
        content of the :http:header:`Allow` response header.

        """
        self.set_header('Allow', ','.join(self.SUPPORTED_METHODS))
        self.set_status(204)
