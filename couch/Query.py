from urllib import quote_plus

class Query():
   data = {}
   dataString = ""

   def __init__(self, data = {}):
      if data:
         self.data = data

   def set(self, key, value):
      self.data[key.lower()] = value
      return self

   def get(self, key):
      if key in self.data:
         return self.data[key]

   def toArray(self):
      return self.data

   def toString(self):
      if self.dataString != "":
         return self.dataString
      data = []
      for key, value in self.data.items():
         if value == None:
            continue
         valueType = type(value)
         if valueType is int:
            value = str(value)
         elif valueType is bool:
            value = str(value).lower()
         print key, value
         data.append("%s=%s" % (quote_plus(key), quote_plus(value)))
      self.dataString = "&".join(data) \
         .replace("%5B", "[").replace("%5D", "]")
      return self.dataString

   def skip(self, num):
      self.data["skip"] = num
      return self

   def limit(self, num):
      self.data["limit"] = num
      return self

