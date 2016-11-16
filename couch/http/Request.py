# -*- coding: utf-8 -*-
# Copyright 2015 Kerem Güneş
#    <k-gun@mail.com>
#
# Apache License, Version 2.0
#    <http://www.apache.org/licenses/LICENSE-2.0>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket

import couch
import couch.util.Util as util

from . Stream import Stream

class Request(Stream):
   """
   Request object.

   @module couch.http
   @object couch.http.Request
   @author Kerem Güneş <k-gun@mail.com>
   """

   # Request methods.
   # @var str
   METHOD_HEAD   = "HEAD"
   METHOD_GET    = "GET"
   METHOD_POST   = "POST"
   METHOD_PUT    = "PUT"
   METHOD_DELETE = "DELETE"
   METHOD_COPY   = "COPY"

   # Client object.
   # @var couch.http.Client
   client = None

   # Request method.
   # @var str
   method = None

   # Request URI.
   # @var str
   uri = None

   def __init__(self, client):
      """
      Object constructor.

      @param (couch.Client) client
      """
      self.type = Stream.TYPE_REQUEST
      self.httpVersion = "1.0"


      self.client = client

      # reset headers (for each "extends" operation, interesting..)
      self.headers = {}

      # set default headers
      self.headers["Host"] = "%s:%s" % (self.client.host, self.client.port)
      self.headers["Connection"] = "close"
      self.headers["Accept"] = "application/json"
      self.headers["Content-Type"] = "application/json"
      self.headers["User-Agent"] = "%s/v%s (+http://github.com/yay-couch/couch-py)" % \
         (couch.Couch.NAME, couch.Couch.VERSION)

      # set basic authorization header
      if self.client.username and self.client.password:
         self.headers["Authorization"] = "Basic "+ \
            util.base64Encode(self.client.username +":"+ self.client.password)

   def setMethod(self, method):
      """
      Set request method.

      @param  (str) method
      @return (self)
      """
      self.method = method.upper()
      if (self.method != Request.METHOD_HEAD
         and self.method != Request.METHOD_GET
         and self.method != Request.METHOD_POST):
         self.setHeader("X-HTTP-Method-Override", self.method)

      return self

   def setUri(self, uri, uriParams = {}):
      """
      Set request URI.

      @param  (str) method
      @return (self)
      """
      self.uri = uri
      if uriParams:
         query = couch.Query(uriParams).toString()
         if query != "":
            self.uri += "?"+ query

      return self

   def send(self, body = None):
      """
      Send.

      @param  (str) method
      @return (str)
      """
      url = util.urlParse(self.uri)
      sock, err = None, None
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
            if not buff: # eof
               break
            recv += buff
      except Exception as e:
         err = e
      finally:
         if sock:
            sock.close()

      # dump whole http messages (request/response)
      if self.client.couch.DEBUG == True:
         print(send)
         print(recv)
         if err:
            raise err

      return recv

   def setBody(self, body = None):
      """
      Set body.

      @param  (mixed) body
      @return (self)
      """
      if (body != None
         and self.method != Request.METHOD_HEAD
         and self.method != Request.METHOD_GET):
         # decode if provided
         if self.getHeader("Content-Type") == "application/json":
            body = util.jsonEncode(body)

         self.body = body
         self.headers["Content-Length"] = len(body)

      return self

   def toString(self):
      """
      String wrap.

      @return (str)
      """
      url = util.urlParse(self.uri)

      return super(Request, self).toString(
         "%s %s?%s HTTP/%s\r\n" % (self.method, url.path, url.query, self.httpVersion))
