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

import os, binascii
from time import time
from math import trunc

class Uuid():
   """
   Uuid object.

   @module couch
   @object couch.Uuid
   @author Kerem Güneş <k-gun@mail.com>
   """

   # UUID limits.
   # @const int
   HEX_8     = 8
   HEX_32    = 32
   HEX_40    = 40
   TIMESTAMP = 0

   # UUID value.
   # @var str|int
   value = None

   def __init__(self, value = None):
      """
      Object constructor.

      @param (mixed) value
      """

      # true is trigger for self.generate() method
      if value == True:
         value = generate(Uuid.HEX_32)

      self.setValue(value)

   def __str__(self):
      """
      Alias of self.getValue() method.

      @return (str|int)
      """
      return self.getValue()

   def setValue(self, value):
      """
      Set value.

      @param  (str|int) value
      @return (None)
      """
      self.value = value

   def getValue(self):
      """
      Get value.

      @param (str|int) value
      """
      return self.value

   @staticmethod
   def generate(limit):
      """
      Generate UUID.

      @param  (int) limit
      @return (str|int)
      @raises (Exception)
      @todo   Implement RFC-4122.
      """

      # simply unix timestamp
      if limit == Uuid.TIMESTAMP:
         return trunc(time())

      if (limit == Uuid.HEX_8
         or limit == Uuid.HEX_32
         or limit == Uuid.HEX_40):
         return binascii.b2a_hex(os.urandom(limit / 2))

      raise Exception("Unimplemented limit given, only 0 or 8|32|40 available!")
