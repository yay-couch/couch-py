import socket

import couch
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
      self.headers["Host"] = "%s:%s" % (self.client.host, self.client.port)
      self.headers["Connection"] = "close"
      self.headers["Accept"] = "application/json"
      self.headers["Content-Type"] = "application/json"
      self.headers["User-Agent"] = "%s/v%s (+http://github.com/qeremy/couch-py)" % \
         (couch.Couch.NAME, couch.Couch.VERSION)

   def setMethod(self, method):
      self.method = method.upper()
      if (self.method != Request.METHOD_HEAD
         and self.method != Request.METHOD_GET
         and self.method != Request.METHOD_POST):
         self.setHeader("X-HTTP-Method-Override", self.method);
      return self

   def setUri(self, uri, uriParams={}):
      self.uri = uri
      if uriParams:
         query = util.urlQuery(uriParams)
         if query:
            self.uri += "?"+ query
      return self

   def send(self, body=None):
      url = util.urlParse(self.uri)

      sock, errr = None, None
      send, recv = "", ""
      send += "%s %s?%s HTTP/%s\r\n" % (self.method, url.path, url.query, self.httpVersion)
      for key, value in self.headers.items():
         if value != None:
            send += "%s: %s\r\n" % (key, value)
      send += "\r\n"
      send += self.getBody() or ""
      try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.connect((self.client.host, self.client.port))
         sock.sendall(send)
         while True:
            buff = sock.recv(1024)
            if buff == "":
               break
            recv += buff
      except Exception as e:
         errr = e
      finally:
         if sock: sock.close()

      # if debug == True @todo
      if 1:
         print send
         print recv
         if errr:
            raise errr

      return recv

   def setBody(self, body=None):
      if (body != None
         and self.method != Request.METHOD_HEAD
         and self.method != Request.METHOD_GET):
         if self.getHeader("Content-Type") == "application/json":
            body = "json"
         self.body = body
         self.headers["Content-Length"] = len(self.body)
      return self

Request.METHOD_HEAD   = "HEAD"
Request.METHOD_GET    = "GET"
Request.METHOD_POST   = "POST"
Request.METHOD_PUT    = "PUT"
Request.METHOD_DELETE = "DELETE"
Request.METHOD_COPY   = "COPY"
