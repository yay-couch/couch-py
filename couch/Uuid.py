import os, binascii
from time import time
from math import trunc

class Uuid():
   value = None
   def __init__(self, value=None):
      if value == True:
         value = generate(Uuid.HEX_32)
      self.setValue(value)
   def __str__(self):
      return self.getValue()

   def setValue(self, value):
      self.value = value
   def getValue(self):
      return self.value

   @staticmethod
   def generate(limit):
      if limit == Uuid.TIMESTAMP:
         return trunc(time())
      if (limit == Uuid.HEX_8
         or limit == Uuid.HEX_32
         or limit == Uuid.HEX_40):
         return binascii.b2a_hex(os.urandom(limit / 2))
      raise Exception("Unimplemented limit given, only 0 or 8|32|40 available!")

Uuid.HEX_8 = 8
Uuid.HEX_32 = 32
Uuid.HEX_40 = 40
Uuid.TIMESTAMP = 0
