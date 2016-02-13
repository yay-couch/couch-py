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

from Stream import Stream

class Response(Stream):
   status = None
   statusCode = 0
   statusText = ""
   def __init__(self):
      self.type = Stream.TYPE_RESPONSE
      self.httpVersion = "1.0"
      self.headers = {}

   def setStatus(self, status):
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
      self.statusCode = int(statusCode)

   def setStatusText(self, statusText):
      self.statusText = statusText.strip()

   def getStatus(self):
      return self.status

   def getStatusCode(self):
      return self.statusCode

   def getStatusText(self):
      return self.statusText

   def setBody(self, body):
      if body != None:
         self.body = body

   def toString(self):
      return super(Response, self).toString(
         "HTTP/%s %s %s\r\n" % (self.httpVersion, self.statusCode, self.statusText))

Response.STATUS = {
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
