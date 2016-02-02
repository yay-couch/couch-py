import re
import couch.http.Request as Request
import couch.http.Response as Response
import couch.util.Util as util

class Client():
   couch = None
   host = "localhost"
   port = 5984
   username = ""
   password = ""
   Request = None
   Response = None

   def __init__(self, couch):
      self.couch = couch
      config = self.couch.getConfig()
      if "host" in config: self.host = config.host
      if "port" in config: self.port = config.port
      if "username" in config: self.username = config.username
      if "password" in config: self.password = config.password

   def getRequest(self):
      return self.Request

   def getResponse(self):
      return self.Response

   def request(self, uri, uriParams={}, body=None, headers={}):
      r = re.match("^([A-Z]+)\s+(/.*)", uri)
      if not r:
         raise Exception("Usage: <REQUEST METHOD> <REQUEST URI>!")
      m = r.groups()
      if len(m) < 2:
         raise Exception("Usage: <REQUEST METHOD> <REQUEST URI>!")
      self.Request = Request(self)
      self.Response = Response()
      uri = "%s:%s/%s" % (self.host, self.port, m[1].strip(" /"))
      self.Request \
         .setMethod(m[0]) \
         .setUri(uri, uriParams)
      for key, value in headers.items():
         self.Request.setHeader(key, value)
      self.Request.setBody(body)

      result = self.Request.send()
      if result != "":
         headers, body = result.split("\r\n\r\n", 1)
         headers = util.parseHeaders(headers)
         if headers:
            for key, value in headers.items():
               if key == "0":
                  self.Response.setStatus(value)
               self.Response.setHeader(key, value)
         self.Response.setBody(body)
      if self.Response.getStatusCode() >= 200:
         self.Response.setError()
      return self.Response

   def head(self, uri, uriParams={}, headers={}):
      return self.request(Request.METHOD_HEAD +" /"+ uri, uriParams, None, headers)

   def get(self, uri, uriParams={}, headers={}):
      return self.request(Request.METHOD_GET +" /"+ uri, uriParams, None, headers)

   def post(self, uri, uriParams={}, body=None, headers={}):
      return self.request(Request.METHOD_POST +" /"+ uri, uriParams, body, headers)

   def put(self, uri, uriParams={}, body=None, headers={}):
      return self.request(Request.METHOD_PUT +" /"+ uri, uriParams, body, headers)

   def delete(self, uri, uriParams={}, headers={}):
      return self.request(Request.METHOD_DELETE +" /"+ uri, uriParams, None, headers)

   def copy(self, uri, uriParams={}, headers={}):
      return self.request(Request.METHOD_COPY +" /"+ uri, uriParams, None, headers)
