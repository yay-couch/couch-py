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

import re

from . Stream import Stream

class Response(Stream):
   """
   Response object.

   @module couch.http
   @object couch.http.Response
   @author Kerem Güneş <k-gun@mail.com>
   """

   # Response statuses.
   # @const dict
   STATUS = {
      200: "OK",
      201: "Created",
      202: "Accepted",
      304: "Not Modified",
      400: "Bad Request",
      401: "Unauthorized",
      403: "Forbidden",
      404: "Not Found",
      405: "Resource Not Allowed",
      406: "Not Acceptable",
      409: "Conflict",
      412: "Precondition Failed",
      415: "Bad Content Type",
      416: "Requested Range Not Satisfiable",
      417: "Expectation Failed",
      500: "Internal Server Error",
   }

   # Response status.
   # @var str
   status = None

   # Response status code.
   # @var int
   statusCode = 0

   # Response status text.
   # @var str
   statusText = ""

   def __init__(self):
      """
      Object constructor.
      """
      self.type = Stream.TYPE_RESPONSE
      self.httpVersion = "1.0"

      # reset headers (for each "extends" operation, interesting..)
      self.headers = {}

   def setStatus(self, status):
      """
      Set status.

      @param  (str) status
      @return (None)
      """
      r = re.match("^HTTP/(\d+\.\d+)\s+(\d+)\s+(.+)", status)
      if not r:
         return

      self.status = status.strip()

      m = r.groups()
      if len(m) == 3:
         self.httpVersion = m[0]
         self.setStatusCode(m[1])
         self.setStatusText(m[2])

   def setStatusCode(self, statusCode):
      """
      Set status code.

      @param  (int) statusCode
      @return (None)
      """
      self.statusCode = int(statusCode)

   def setStatusText(self, statusText):
      """
      Set status text.

      @param  (str) statusText
      @return (None)
      """
      self.statusText = statusText.strip()

   def getStatus(self):
      """
      Get status.

      @return (str)
      """
      return self.status

   def getStatusCode(self):
      """
      Get status code.

      @return (int)
      """
      return self.statusCode

   def getStatusText(self):
      """
      Get status text.

      @return (str)
      """
      return self.statusText

   def setBody(self, body):
      """
      Set body.

      @param  (str) body
      @return (None)
      """
      if body != None:
         self.body = body

   def toString(self):
      """
      String wrap.

      @return (str)
      """
      return super(Response, self).toString(
         "HTTP/%s %s %s\r\n" % (self.httpVersion, self.statusCode, self.statusText))
