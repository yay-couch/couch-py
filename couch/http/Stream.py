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

import couch.util.Util as util

class Stream(object):
   """
   Stream object.

   @module couch.http
   @object couch.http.Stream
   @author Kerem Güneş <qeremy[at]gmail[dot]com>
   """

   # Stream types.
   # @const int
   TYPE_REQUEST  = 1
   TYPE_RESPONSE = 2

   # Stream type that used in self.toString().
   # @var int
   type = None

   # HTTP version.
   # @var str
   httpVersion = None

   # Stream headers.
   # @var dict
   headers = {}

   # Stream body.
   # @var mixed
   body = None

   # Error string & data.
   # @var str, dict
   error, errorData = None, {}

   def __init__(self, headers = {}, body = None):
      """
      Object constructor.

      @param  {dict}  headers
      @param  {mixed} body
      """
      self.headers = headers
      self.body    = body

   def __str__(self):
      """
      String wrap.

      @return {str}
      """
      return self.toString()

   def setBody(self, body = None):
      """
      Set body.

      @return {str}
      @raises {Exception}
      @abstract
      """
      if self.__class__.__name__ == "Stream":
         raise Exception("You should re-define [<OBJECT>].setBody(self, body=None) method!")

   def getBody(self):
      """
      Get body

      @return {str}
      """
      return self.body

   def getBodyData(self, key = None):
      """
      Get body data (parsed).

      @param  {str} key
      """
      bodyData = {}
      # should parsed?
      if self.getHeader("Content-Type") == "application/json":
         bodyData = util.jsonDecode(self.body or "")
         if key != None:
            return util.dig(key, bodyData)

      return bodyData

   def setHeader(self, key, value = None):
      """
      Set header.

      @param  {str} key
      @param  {str} value
      @return {None}
      """
      # None = delete
      if value == None:
         if key in self.headers:
            del self.headers[key]
      else:
         self.headers[key] = value

   def getHeader(self, key):
      """
      Get header.

      @param  {str} key
      @return {mixed}
      """
      if key in self.headers:
         return self.headers[key]

   def getHeaderAll(self):
      """
      Get all headers.

      @return {dict}
      """
      return self.headers

   def setError(self, body = None):
      """
      Set error.

      @param  {mixed} body
      @return {None}
      """
      body = util.jsonDecode(body or self.body or "")
      if type(body) is dict and ("error" in body) and ("reason" in body):
         self.error = "Stream Error >> error: '%s', reason: '%s'" % \
            (body["error"], body["reason"])
         self.errorData["error"] = body["error"]
         self.errorData["reason"] = body["reason"]

   def getError(self):
      """
      Get error.

      @return {dict}
      """
      return self.error

   def toString(self, firstLine):
      """
      Get stream as string.

      @param  {str} firstLine
      @return {str}
      """
      ret = firstLine
      for key, value in self.headers.items():
         if value != None:
            if key == "0":
               continue

            ret += "%s: %s\r\n" % (key, value)

      ret += "\r\n"
      ret += self.getBody() or ""

      return ret
