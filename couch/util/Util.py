import re
import json
import pprint
from urllib import urlencode
from urlparse import urlparse

def pre(o):
   pprint.pprint(o)

def prd(o, all=False):
   name = getObjectName(o)
   for attr in dir(o):
      # show only attrs
      if all == False and attr[:2] != "__":
         print "<%s>.%s = %s" % (name, attr, getattr(o, attr))
      elif all == True:
         print "<%s>.%s = %s" % (name, attr, getattr(o, attr))

def getObjectName(o):
   name = "%s" % (o)
   name = name[1:name.find(" ")]
   return name

def parseHeaders(headers):
   ret = {}
   tmp = headers.split("\r\n")
   if tmp:
      # status line (HTTP/1.0 200 OK)
      ret["0"] = tmp.pop(0)
      for tm in tmp:
         t = tm.split(":", 2)
         if len(t) == 2:
            ret[t[0].strip()] = t[1].strip()
   return ret

def jsonEncode(input):
   try:
      return json.dumps(input)
   except Exception: pass
def jsonDecode(input):
   try:
      return json.loads(input)
   except Exception: pass

def urlQuery(query):
   return urlencode(query)
def urlParse(url):
   if not re.match("^https?://", url):
      url = "http://"+ url
   return urlparse(url)
