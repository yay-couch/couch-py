import re
import pprint
import urllib
import json, base64
from urlparse import urlparse

def pre(o):
   pprint.pprint(o)

def prd(o, all=False):
   name = o.__class__
   for attrName in dir(o):
      # show only attrs
      attrValue = getattr(o, attrName)
      if all == False and not hasattr(attrValue, '__call__'):
         print "<%s>.%s = %s" % (name, attrName, attrValue)
      elif all == True:
         print "<%s>.%s = %s" % (name, attrName, attrValue)

def dig(key, array):
   if key in array:
      return array[key]
   try:
      keys = key.split(".")
      key  = keys.pop(0)
      if len(keys) > 0:
         return dig(".".join(keys), array[key])
      return array[key]
   except: pass

def parseHeaders(headers):
   ret = {}
   tmp = headers.split("\r\n")
   if tmp:
      # status line (HTTP/1.0 200 OK)
      ret["0"] = tmp.pop(0)
      for tm in tmp:
         t = tm.split(":", 1)
         if len(t) == 2:
            ret[t[0].strip()] = t[1].strip()
   return ret

def jsonEncode(input):
   try:
      return json.dumps(input)
   except: pass
def jsonDecode(input):
   try:
      return json.loads(input)
   except: pass

def base64Encode(input):
   try:
      return base64.b64encode(input)
   except: pass
def base64Decode(input):
   try:
      return base64.b64decode(input)
   except: pass

def urlEncode(input):
   if hasattr(input, "toString") and callable(input.toString):
      input = input.toString()
   return urllib.quote_plus(input)
def urlDecode(input):
   return urllib.unquote_plus(input)

def urlQuery(q):
   qt = type(q)
   if qt is str:
      return urllib.urlencode(q)
   elif qt is dict:
      qs = []
      for key, value in q.items():
         vt = type(value)
         if vt is int:
            value = str(value)
         elif vt is bool:
            value = str(value).lower()
         qs.append("%s=%s" % (urllib.quote_plus(key), urllib.quote_plus(value)))
      return "&".join(qs)

def urlParse(url):
   if not re.match("^https?://", url):
      url = "http://"+ url
   try:
      ret = urlparse(url)
      ret.host = ret.hostname
      return ret
   except:
      return {}

def quote(input):
   return input.replace("\"", "%22")

def isSet(input, path):
   if not input:
      return True
   return (None != dig(input, path))

def isEmpty(input):
   if not input:
      return True
   return (input is None or input is "" or input is 0 or input is 0.00)
