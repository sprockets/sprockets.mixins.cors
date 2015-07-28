Version History
===============

0.1.0
-----
 - initial implementation including:

   - :class:`sprockets.mixins.cors.CORSMixin`
   - :class:`sprockets.mixins.cors.CORSSettings`
   - Support for the following pre-flight request headers:

     - :mailheader:`Origin`
     - :mailheader:`Access-Control-Request-Method`

   - Support for the following pre-flight response headers:

     - :mailheader:`Access-Control-Allow-Origin`
     - :mailheader:`Access-Control-Allow-Methods`
     - :mailheader:`Access-Control-Allow-Credentials`

   - Support for the following in-line response headers:

     - :mailheader:`Access-Control-Allow-Origin`
     - :mailheader:`Access-Control-Allow-Credentials`
