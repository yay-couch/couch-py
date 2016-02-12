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

import os
import re
import pprint
import subprocess
import json, base64
import urllib, urlparse

def pre(o):
   """
   Pretty print.

   @param  {mixed} o
   @return {None}
   """
   pprint.pprint(o)

def prd(o, all = False):
   """
   Pretty dump.

   @param  {object} o
   @param  {bool}   all
   @return {None}
   """
   name = o.__module__
   for attrName in dir(o):
      # show only attrs
      attrValue = getattr(o, attrName)
      if all == False and not hasattr(attrValue, '__call__'):
         print "<%s>.%s = %s" % (name, attrName, attrValue)
      elif all == True:
         print "<%s>.%s = %s" % (name, attrName, attrValue)

def dig(key, array):
   """
   Dict/list exporter.

   @param  {str}       key
   @param  {dict|list} array
   @return {mixed}
   """
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
   """
   Parse headers.

   @param  {str} headers
   @return {dict}
   """
   ret = {}

   tmp = headers.split("\r\n")
   if tmp:
      ret["0"] = tmp.pop(0) # status line
      for tm in tmp:
         t = tm.split(":", 1)
         if len(t) == 2:
            ret[t[0].strip()] = t[1].strip()

   return ret

def jsonEncode(input):
   """
   JSON encode.

   @param  {mixed} input
   @return {str|None}
   """
   try:
      return json.dumps(input)
   except: pass

def jsonDecode(input):
   """
   JSON decode.

   @param  {str} input
   @return {mixed}
   """
   try:
      return json.loads(input)
   except: pass

def base64Encode(input):
   """
   Base64 encode.

   @param  {str} input
   @return {str|None}
   """
   try:
      return base64.b64encode(input)
   except: pass

def base64Decode(input):
   """
   Base64 decode.

   @param  {str} input
   @return {str|None}
   """
   try:
      return base64.b64decode(input)
   except: pass

def urlEncode(input):
   """
   URL encode.

   @param  {str} input
   @return {str}
   """
   # handle objects
   if hasattr(input, "__str__") and callable(input.__str__):
      input = input.__str__()

   return urllib.quote_plus(input)

def urlDecode(input):
   """
   URL decode.

   @param  {str} input
   @return {str}
   """
   return urllib.unquote_plus(input)

def urlParse(url):
   """
   URL parse.

   @param  {str} url
   @return {urlparse.ParseResult|None}
   """
   if not url:
      raise Exception("No valid URL given!")

   # ensure protocol for proper parse
   if not re.match("^https?://", url):
      url = "http://"+ url

   try:
      ret = urlparse.urlparse(url)
      # dear "urlparse" developer(s), please see the link below..
      # https://tools.ietf.org/html/rfc3986#section-3.2.2
      ret.host = ret.hostname

      return ret
   except: pass

def quote(input):
   """
   Quote (escaped quote).

   @param  {str} input
   @return {str}
   """
   return input.replace("\"", "%22")

def basename(path):
   """
   Get basename.

   @param  {str} path
   @return {str}
   """
   return os.path.basename(path)

def fileExists(file):
   """
   Check file exist.

   @param  {str} file
   @return {bool}
   """
   return os.path.isfile(file)

def fileInfo(file):
   """
   Get file info.

   @param  {str} file
   @return {dict}
   @raises {Exception}
   """
   if not fileExists(file):
      raise Exception("Given file does not exist! file: '%s'" % file)

   # set defaults
   info = {
      "mime": None,
      "charset": None,
      "name": None,
      "extension": None,
   }

   info["name"] = basename(file)
   info["extension"] = os.path.splitext(file)[1][1:]

   # use system "file" tool
   try:
      out = subprocess.check_output(["file", "-i", file])
      if out:
         tmp = out.strip().split(" ")
         if len(tmp) == 3:
            mime = tmp[1].strip()
            if mime[-1] == ";":
               mime = mime[:-1]

            info["mime"] = mime
            info["charset"] = tmp[2].strip().split("=")[1]
   except: pass

   return info

def fileGetContents(file, offset = -1, maxlen = -1):
   """
   Get file contents.

   @param  {str} file
   @param  {int} offset
   @param  {int} maxlen
   @return {str}
   """
   if not fileExists(file):
      raise Exception("Given file does not exist! file: '%s'" % file)

   try:
      fp = open(file, "rb")
      # check offset for seek
      if offset > 0:
         fp.seek(offset)

      return fp.read(maxlen)
   finally:
      fp.close()
