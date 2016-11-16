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

try:
   from urllib import quote_plus
except:
   from urllib.parse import quote_plus

class Query():
   """
   Query object.

   @module couch
   @object couch.Query
   @author Kerem Güneş <k-gun@mail.com>
   """

   # Query data & string.
   # @var array, string
   data = {}
   dataString = ""

   def __init__(self, data = {}):
      """
      Object constructor.

      @param (dict) data
      """
      if data:
         self.data = data

   def set(self, key, value):
      """
      Set query param.

      @param  (str)   key
      @param  (mixed) value
      @return (self)
      """
      self.data[key.lower()] = value

      return self

   def get(self, key):
      """
      Get query param.

      @param  (str) key
      @return (mixed)
      """
      if key in self.data:
         return self.data[key]

   def toArray(self):
      """
      Get query params as list.

      @return (list)
      """
      return self.data

   def toString(self):
      """
      Get query params as string.

      @return (str)
      """

      # check if already generated before
      if self.dataString != "":
         return self.dataString

      data = []
      for key, value in self.data.items():
         if value is None:
            continue

         valueType = type(value)
         if valueType is int:
            value = str(value)
         elif valueType is bool:
            # proper CouchDB booleans
            value = str(value).lower()

         data.append("%s=%s" % (quote_plus(key), quote_plus(value)))

      self.dataString = "&".join(data) \
         .replace("%5B", "[").replace("%5D", "]")

      return self.dataString

   def skip(self, num):
      """
      Add skip param to query data.

      @param (int) num
      """
      self.data["skip"] = num

      return self

   def limit(self, num):
      """
      Add limit param to query data.

      @param (int) num
      """
      self.data["limit"] = num

      return self

