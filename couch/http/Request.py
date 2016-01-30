import socket
from urllib import urlencode

import couch.util.Util as util
from Stream import Stream

class Request(Stream):
   client = None
   method = None
   uri = None
   def __init__(self, client):
      self.type = Stream.TYPE["REQUEST"];
      self.httpVersion = "1.0";

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
      error = None
      send, recv = "", ""
      send += "GET / HTTP/%s\r\n" % (self.httpVersion)
      send += "Host: localhost\r\n"
      send += "Connection: close\r\n"
      send += "Accept: application/json\r\n"
      send += "\r\n"
      send += self.getBody() or ""
      try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.connect(("localhost", 5984))
         sock.sendall(send)
         while True:
            buff = sock.recv(1024)
            if buff == "":
               break
            recv += buff
      except Exception, e:
         error = e
      finally:
         sock.close()

      # if debug == True
      if 1:
         print send
         print recv
         if error:
            raise error

      return recv

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
