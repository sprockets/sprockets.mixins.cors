sprockets.mixins.cors
=====================
This library exposes a mix-in that adds some useful CORS_ hooks over
a basic ``tornado.web.RequestHandler``.

Example Usage
-------------

.. code-block:: python

   from tornado import web
   from sprockets.mixins import cors

   class MyHandler(cors.CORSMixin, web.RequestHandler):
   
       def initialize(self):
           super(MyHandler, self).initialize()
           self.cors.allowed_methods.add('GET')
           self.cors.allowed_origins.add('http://my.frontend.site')
