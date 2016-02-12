# -*- coding: utf-8 -*-
# Copyright 2015 Kerem Güneş
#    <http://qeremy.com>
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

import re
import couch.http.Request as Request
import couch.http.Response as Response
import couch.util.Util as util

class Client():
   """
   Client object.

   @module couch
   @object couch.Client
   @author Kerem Güneş <qeremy[at]gmail[dot]com>
   """

   # Couch object.
   # @var couch.Couch
   couch = None

   # CouchDB host
   # @var str
   host = "localhost"

   # CouchDB port
   # @var int
   port = 5984

   # CouchDB username & password that used in connections if provided.
   # @var str, str
   username, password = "", ""

   # Request, Response objects.
   # @var couch.http.Request, couch.http.Response
   Request, Response = None, None

   def __init__(self, couch):
      """
      Object constructor.

      @param {couch.Couch} couch
      """
      self.couch = couch

      # use config if provided
      config = self.couch.getConfig()

      # set host & port
      if "host" in config:
         self.host = config.host
      if "port" in config:
         self.port = config.port

      # set credentials
      if "username" in config:
         self.username = config.username
      if "password" in config:
         self.password = config.password

   def getRequest(self):
      """
      Get Request object.

      @return {couch.http.Request}
      """
      return self.Request

   def getResponse(self):
      """
      Get Response object.

      @return {couch.http.Response}
      """
      return self.Response

   def request(self, uri, uriParams = {}, body = None, headers = {}):
      """
      Make a HTTP request using Request and return Response.

      @param  {str}   uri
      @param  {dict}  uriParams
      @param  {mixed} body
      @param  {dict}  headers
      @return {couch.http.Response}
      @throws {Exception}
      """
      # match for a valid request i.e: HEAD /foo
      r = re.match("^([A-Z]+)\s+(/.*)", uri)
      if not r:
         raise Exception("Usage: <REQUEST METHOD> <REQUEST URI>!")

      m = r.groups()
      if len(m) < 2:
         raise Exception("Usage: <REQUEST METHOD> <REQUEST URI>!")

      self.Request = Request(self)
      self.Response = Response()

      # merge host, port and uri
      uri = "%s:%s/%s" % (self.host, self.port, m[1].strip(" /"))

      # set request method, uri, body
      self.Request \
         .setMethod(m[0]) \
         .setUri(uri, uriParams) \
         .setBody(body)

      # set request headers (if any)
      for key, value in headers.items():
         self.Request.setHeader(key, value)

      result = self.Request.send()
      if result != "":
         headers, body = result.split("\r\n\r\n", 1)
         headers = util.parseHeaders(headers)
         if headers:
            for key, value in headers.items():
               # status line
               if key == "0":
                  self.Response.setStatus(value)
               self.Response.setHeader(key, value)
         self.Response.setBody(body)

      # is error?
      if self.Response.getStatusCode() >= 200:
         self.Response.setError()

      return self.Response

   def head(self, uri, uriParams = {}, headers = {}):
      """
      Make a HEAD request (i.e HEAD /foo).

      @param  {str}  uri
      @param  {dict} uriParams
      @param  {dict} headers
      @return {couch.http.Response}
      @throws {Exception}
      """
      return self.request(Request.METHOD_HEAD +" /"+ uri, uriParams, None, headers)

   def get(self, uri, uriParams = {}, headers = {}):
      """
      Make a GET request (i.e GET /foo).

      @param  {str}  uri
      @param  {dict} uriParams
      @param  {dict} headers
      @return {couch.http.Response}
      @throws {Exception}
      """
      return self.request(Request.METHOD_GET +" /"+ uri, uriParams, None, headers)

   def post(self, uri, uriParams = {}, body = None, headers = {}):
      """
      Make a POST request (i.e POST /foo).

      @param  {str}   uri
      @param  {dict}  uriParams
      @param  {mixed} body
      @param  {dict}  headers
      @return {couch.http.Response}
      @throws {Exception}
      """
      return self.request(Request.METHOD_POST +" /"+ uri, uriParams, body, headers)

   def put(self, uri, uriParams = {}, body = None, headers = {}):
      """
      Make a PUT request (i.e PUT /foo).

      @param  {str}   uri
      @param  {dict}  uriParams
      @param  {mixed} body
      @param  {dict}  headers
      @return {couch.http.Response}
      @throws {Exception}
      """
      return self.request(Request.METHOD_PUT +" /"+ uri, uriParams, body, headers)

   def delete(self, uri, uriParams = {}, headers = {}):
      """
      Make a DELETE request (i.e DELETE /foo).

      @param  {str}  uri
      @param  {dict} uriParams
      @param  {dict} headers
      @return {couch.http.Response}
      @throws {Exception}
      """
      return self.request(Request.METHOD_DELETE +" /"+ uri, uriParams, None, headers)

   def copy(self, uri, uriParams = {}, headers = {}):
      """
      Make a COPY request (i.e COPY /foo).

      @param  {str}  uri
      @param  {dict} uriParams
      @param  {dict} headers
      @return {couch.http.Response}
      @throws {Exception}
      """
      return self.request(Request.METHOD_COPY +" /"+ uri, uriParams, None, headers)
