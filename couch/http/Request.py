from urllib import urlencode
from Stream import Stream

class Request(Stream):
   client = None
   method = None
   uri = None
   def __init__(self, client):
      self.type = Stream.TYPE["REQUEST"];
      self.httpVersion = "1.1";

      self.client = client

   def setMethod(self, method):
      self.method = method.upper()
      if (self.method != Request.METHOD["HEAD"]
         and self.method != Request.METHOD["GET"]
         and self.method != Request.METHOD["POST"]):
         self.setHeader("X-HTTP-Method-Override", self.method);
      return self

   def setUri(self, uri, uriParams={}):
      self.uri = uri
      if uriParams:
         query = urlencode(uriParams)
         if query:
            self.uri += "?"+ query
      return self

   def send(self, body=None):
      pass

   def setBody(self, body=None):
      if (body != None
         and self.method != Request.METHOD["HEAD"]
         and self.method != Request.METHOD["GET"]):
         if self.getHeader("Content-Type") == "application/json":
            body = "json"
         self.body = body
         self.headers["Content-Length"] = len(self.body)
      return self

Request.METHOD = {
    "HEAD": "HEAD",
     "GET": "GET",
    "POST": "POST",
     "PUT": "PUT",
  "DELETE": "DELETE",
    "COPY": "COPY"
};
