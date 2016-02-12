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

import couch
import couch.util.Util as util

class DocumentAttachment(object):
   """
   DocumentAttachment object.

   @module couch
   @object couch.DocumentAttachment
   @author Kerem Güneş <qeremy[at]gmail[dot]com>
   """

   # Owner document
   # @var couch.Document
   document = None

   # Abstract file path & file name.
   # @var {str}, {str}
   file, fileName = None, None

   # Attachment file contents, contents length.
   # @var {int}, {int}
   data, dataLength = None, 0

   # Attachment mime.
   # @var {str}
   contentType = None

   # CouchDB file digest.
   # @var {str}
   digest = None

   def __init__(self, document = None, file = None, fileName = None):
      """
      Object constructor.

      @param {couch.Document} document
      @param {str}            file
      @param {str}            fileName
      """
      if document:
         self.setDocument(document)

      if file:
         self.file = file
         self.fileName = fileName if fileName else util.basename(file)

   def __setattr__(self, name, value):
      """
      Setter for magic actions.

      @param  {str} name
      @param  {str} value
      @return {None}
      @raises {Exception}
      """
      if not hasattr(self, name):
         raise Exception("`%s` property does not exists on this object!" % name)

      # file is exception
      if name == "file":
         super.__setattr__(self, "file", value)
         super.__setattr__(self, "fileName", util.basename(value))
      else:
         super.__setattr__(self, name, value)

   def __getattr__(self, name):
      """
      Getter for magic actions.

      @param  {str} name
      @return {mixed}
      @raises {Exception}
      """
      if not hasattr(self, name):
         raise Exception("`%s` property does not exists on this object!" % name)

      return super.__getattr__(self, name)

   def setDocument(self, document):
      """
      Set owner document.

      @param  {couch.Document} document
      @return {None}
      @raises {Exception}
      """
      if not isinstance(document, couch.Document):
         raise Exception("'document' arg must be instance of couch.Document")

      super.__setattr__(self, "document", document)

   def getDocument(self):
      """
      Get owner document.

      @return {couch.Document}
      """
      return self.document

   def ping(self, *args):
      """
      Ping a document attachment.

      @param  {list} args int Expected status code
      @return {bool}
      @raises {Exception}
      """
      if not self.document:
         raise Exception("Attachment document is not defined!")

      docId = self.document.getId()
      docRev = self.document.getRev()

      if not docId:
         raise Exception("Attachment document _id is required!")

      if not self.fileName:
         raise Exception("Attachment file name is required!")

      query, headers = {}, {}
      if docRev:
         query["rev"] = docRev
      if self.digest:
         headers["If-None-Match"] = '"%s"' % (self.digest)

      database = self.document.getDatabase()
      response = database.client.head("%s/%s/%s" %
         (database.name, util.urlEncode(docId), util.urlEncode(self.fileName)), query, headers)

      return response.getStatusCode() in (args or [200])

   def find(self):
      """
      Find attachment.

      @return {mixed|None}
      @raises {Exception}
      """
      if not self.document:
         raise Exception("Attachment document is not defined!")

      docId = self.document.getId()
      docRev = self.document.getRev()

      if not docId:
         raise Exception("Attachment document _id is required!")

      if not self.fileName:
         raise Exception("Attachment file name is required!")

      query = {}
      if docRev:
         query["rev"] = docRev

      headers = {}
      headers["Accept"] = "*/*"
      headers["Content-Type"] = None
      if self.digest:
         headers["If-None-Match"] = '"%s"' % (self.digest)

      database = self.document.getDatabase()
      response = database.client.get("%s/%s/%s" %
         (database.name, util.urlEncode(docId), util.urlEncode(self.fileName)), query, headers)

      # check response status code
      if response.getStatusCode() in [200, 304]:
         ret = {}
         ret["content"] = response.getBody()
         ret["content_type"] = response.getHeader("Content-Type")
         ret["content_length"] = response.getHeader("Content-Length")
         md5 = response.getHeader("Content-MD5")
         if md5:
            ret["digest"] = "md5-"+ md5
         else:
            ret["digest"] = "md5-"+ (response.getHeader("ETag") or "").strip('"')

         return ret

   def save(self):
      """
      Save attachment.

      @return {mixed}
      @raises {Exception}
      """
      if not self.document:
         raise Exception("Attachment document is not defined!")

      docId = self.document.getId()
      docRev = self.document.getRev()

      if not docId:
         raise Exception("Attachment document _id is required!")

      if not docRev:
         raise Exception("Attachment document _rev is required!")

      if not self.fileName:
         raise Exception("Attachment file name is required!")

      # read file data
      self.readFile(False)

      headers = {}
      headers["If-Match"] = docRev
      headers["Content-Type"] = self.contentType

      database = self.document.getDatabase()
      return database.client.put("%s/%s/%s" %
         (database.name, util.urlEncode(docId), util.urlEncode(self.fileName)),
            None, self.data, headers).getBodyData()

   def remove(self, batch = False, fullCommit = False):
      """
      Remove attachment.

      @param  {bool} batch
      @param  {bool} fullCommit
      @return {mixed}
      @raises {Exception}
      """
      if not self.document:
         raise Exception("Attachment document is not defined!")

      docId = self.document.getId()
      docRev = self.document.getRev()

      if not docId:
         raise Exception("Attachment document _id is required!")

      if not docRev:
         raise Exception("Attachment document _rev is required!")

      if not self.fileName:
         raise Exception("Attachment file name is required!")

      batch = "?batch=ok" if batch else ""

      headers = {}
      headers["If-Match"] = docRev
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"

      database = self.document.getDatabase()
      return database.client.delete("%s/%s/%s%s" %
         (database.name, util.urlEncode(docId), util.urlEncode(self.fileName), batch),
            None, headers).getBodyData()

   def toArray(self, encode = True):
      """
      Get attachment data as array that CouchDB expects.

      @param  {bool} encode
      @return {dict}
      """
      # read file first
      self.readFile(encode)

      array = {}
      array["data"] = self.data
      array["content_type"] = self.contentType

      return array

   def toJson(self, encode = True):
      """
      Get attachment data as json string that CouchDB expects.
      @param  {bool} encode
      @return {str}
      """
      return util.jsonEncode(self.toArray(encode))

   def readFile(self, encode = True):
      """
      Read file contents, set attachment data, data length and content type.

      @param  {bool} encode
      @return {None}
      @raises {Exception}
      """
      if not self.file:
         raise Exception("Attachment file is empty!")

      # detect content type
      info = util.fileInfo(self.file)
      self.contentType = info["mime"]

      data = util.fileGetContents(self.file)
      self.data = data
      if encode:
         self.data = util.base64Encode(data)

      self.dataLength = len(data)

