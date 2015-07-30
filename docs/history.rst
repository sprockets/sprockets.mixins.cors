Version History
===============

`0.1.1`_
--------
 - minor packaging changes

`0.1.0`_
--------
 - initial implementation including:

   - :class:`sprockets.mixins.cors.CORSMixin`
   - :class:`sprockets.mixins.cors.CORSSettings`
   - Support for the following pre-flight request headers:

     - :mailheader:`Origin`
     - :mailheader:`Access-Control-Request-Method`
     - :mailheader:`Access-Control-Request-Headers`

   - Support for the following pre-flight response headers:

     - :mailheader:`Access-Control-Allow-Origin`
     - :mailheader:`Access-Control-Allow-Methods`
     - :mailheader:`Access-Control-Allow-Credentials`
     - :mailheader:`Access-Control-Allow-Headers`

   - Support for the following in-line response headers:

     - :mailheader:`Access-Control-Allow-Origin`
     - :mailheader:`Access-Control-Allow-Credentials`

.. _0.1.1: https://github.com/sprockets/sprockets.mixins.cors/compare/0.1.0...0.1.1
.. _0.1.0: https://github.com/sprockets/sprockets.mixins.cors/compare/0.0.0...0.1.0
