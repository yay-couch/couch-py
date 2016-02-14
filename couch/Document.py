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

import couch
import couch.util.Util as util

class Document(object):
   """
   Document object.

   @module couch
   @object couch.Document
   @author Kerem Güneş <k-gun@mail.com>
   """

   # Document ID & document revision ID.
   # @var {str}, {str}
   id, rev = None, None

   # Delete(d) flag.
   # @var {bool}
   deleted = False

   # Document attachments.
   # @var {dict}
   attachments = {}

   # Database object.
   # @var {couch.Database}
   database = None

   # Document data.
   # @var {dict}
   data = {}

   def __init__(self, database = None, data = {}):
      """
      Object constructor.

      @param  {couch.Database} database
      @param  {dict}           data
      """
      if database:
         self.setDatabase(database)

      if data:
         self.setData(data)

   def __setattr__(self, key, value):
      """
      Setter method for magic actions.

      @param  {str}   key
      @param  {mixed} value
      @return {None}
      """
      self.setData({key: value})

   def __getattr__(self, key):
      """
      Getter method for magic actions.

      @param  {str} key
      @return {mixed}
      """
      return self.getData(key)

   def setDatabase(self, database):
      """
      Set document database.

      @param  {couch.Database} database
      @return {None}
      @raises {Exception}
      """
      if not isinstance(database, couch.Database):
         raise Exception("'database' arg must be instance of couch.Database")

      super.__setattr__(self, "database", database)

   def getDatabase(self):
      """
      Get document database.

      @return {couch.Database}
      """
      return self.database

   def setId(self, id):
      """
      Set document ID.

      @param  {couch.Uuid|str} id
      @return {None}
      """
      if not isinstance(id, couch.Uuid):
         id = couch.Uuid(id)

      super.__setattr__(self, "id", id)

   def setRev(self, rev):
      """
      Set document revision ID.

      @param  {str} rev
      @return {None}
      """
      super.__setattr__(self, "rev", rev)

   def setDeleted(self, deleted):
      """
      Set deleted flag.

      @param  {bool} deleted
      @return {None}
      """
      super.__setattr__(self, "deleted", bool(deleted))

   def getId(self):
      """
      Get document ID.

      @return {couch.Uuid|str|None}
      """
      return self.id

   def getRev(self):
      """
      Get document revision ID.

      @return {str|None}
      """
      return self.rev

   def getDeleted(self):
      """
      Get deleted flag.

      @return {bool}
      """
      return self.deleted

   def setAttachment(self, attachment):
      """
      Add an attachment to document object.

      @param  {couch.DocumentAttachment|dict} attachment
      @return {None}
      @raises {Exception}
      """
      if not isinstance(attachment, couch.Attachment):
         if "file" not in attachment:
            raise Exception("Attachment file is required!")

         file = attachment["file"]
         fileName = attachment["file_name"] or None
         attachment = DocumentAttachment(self, file, fileName)

      if "_attachments" not in self.data:
         self.data["_attachments"] = {}

      # check if attachment is duplicate
      if attachment.fileName in self.data["_attachments"]:
         raise Exception("Attachment is alredy exists on this document!")

      self.attachments[attachment.fileName] = \
         self.data["_attachments"][attachment.fileName] = attachment

   def getAttachment(self, name):
      """
      Get a document attachment by name.

      @param  {str} name
      @return {couch.DocumentAttachment|None}
      """
      if name in self.attachments[name]:
         return self.attachments[name]

   def getAttachmentAll(self):
      """
      Get all attachments.

      @return {dict}
      """
      return self.attachments

   def unsetAttachment(self, name):
      """
      Unset an attachment.

      @param  {str} name
      @return {None}
      """
      if name in self.attachments[name]:
         del self.attachments[name]

   def unsetAttachmentAll(self):
      """
      Dump all document attachments.

      @return {None}
      """
      self.attachments = {}

   def setData(self, data = {}):
      """
      Set document data.

      @param  {dict} data
      @return {None}
      """
      # set special properties
      if "_id" in data: self.setId(data["_id"])
      if "_rev" in data: self.setRev(data["_rev"])
      if "_deleted" in data: self.setDeleted(data["_deleted"])
      if "_attachments" in data:
         # add attachments and remove it so prevent to add into data array
         for attachment in data["_attachments"]:
            self.setAttachment(attachment)

         del data["_attachments"]

      for key, value in data.items():
         self.data[key] = value

   def getData(self, key = None):
      """
      Get document data value.

      @param  {str} key
      @return {mixed}
      """
      if key != None:
         return util.dig(key, self.data)

      return self.data

   def ping(self, *args):
      """
      Ping document.

      @param  {int} *args Expected status code(s).
      @return {bool}
      @raises {Exception}
      """
      if not self.id:
         raise Exception("_id field is could not be empty!")

      headers = {}
      if self.rev != None:
         headers["If-None-Match"] = '"%s"' % (self.rev)

      response = self.database.client.head(self.database.name +"/"+
         util.urlEncode(self.id), None, headers)

      return response.getStatusCode() in (args or [200])

   def isExists(self):
      """
      Check document if exists that server may return 200|304 status codes.

      @return bool
      """
      return self.ping(200, 304)

   def isNotModified(self):
      """
      Check document if not modified.

      @return {bool}
      @raises {Exception}
      """
      if not self.rev:
         raise Exception("_rev field could not be empty!")

      return self.ping(304)

   def find(self, query = {}):
      """
      Find a document.

      @param  {dict} query
      @return {mixed}
      @raises {Exception}
      """
      if not self.id:
         raise Exception("_id field is could not be empty!")

      query = query or {}
      if "rev" not in query and self.rev:
         query["rev"] = self.rev

      return self.database.client.get(self.database.name +"/"+
         util.urlEncode(self.id), query).getBodyData()

   def findRevisions(self):
      """
      Find a document's revisions.

      @return {dict|None}
      """
      return util.dig("_revisions", self.find({"revs": True}))

   def findRevisionsExtended(self):
      """
      Find a document's revisions as extended result.

      @return {dict|None}
      """
      return util.dig("_revs_info", self.find({"revs_info": True}))

   def findAttachments(self, attEncInfo = False, attsSince = []):
      """
      Find a document's attachments.

      @param  {bool}      attEncInfo
      @param  {dict|None} attsSince
      @return {dict|None}
      """
      query = {}
      query["attachments"] = True
      query["att_encoding_info"] = attEncInfo

      if attsSince:
         attsSinceArray = []
         for attsSinceValue in attsSince:
            attsSinceArray.append('"%s"' % util.quote(attsSinceValue))
         query["atts_since"] = "[%s]" % ",".join(attsSinceArray)

      return util.dig("_attachments", self.find(query))

   def save(self, batch = False, fullCommit = False):
      """
      Create or update a document.

      @param  {bool} batch
      @param  {bool} fullCommit
      @return {mixed}
      """
      batch = "?batch=ok" if batch else ""

      headers = {}
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"
      if self.rev:
         headers["If-Match"] = self.rev

      data = self.getData()
      if self.attachments:
         data["_attachments"] = {}
         for name, attachment in self.attachments.items():
            data["_attachments"][name] = attachment.toArray()

      # insert action
      if not self.id:
         ret = self.database.client.post(self.database.name + batch, None,
            data, headers).getBodyData()
         if ret and ("id" in ret):
            self.setId(ret["id"])
      # update action
      else:
         ret = self.database.client.put(self.database.name +"/"+
            util.urlEncode(self.id) + batch, None, data, headers).getBodyData()

      # for next instant call(s)
      if ret and ("rev" in ret):
         self.setRev(ret["rev"])

      return ret

   def remove(self, batch = False, fullCommit = False):
      """
      Remove a document.

      @param  {bool} batch
      @param  {bool} fullCommit
      @return {mixed}
      @raises {Exception}
      """
      if not self.id and not self.rev:
         raise Exception("Both _id & _rev fields could not be empty!")

      batch = "?batch=ok" if batch else ""

      headers = {}
      headers["If-Match"] = self.rev
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"

      return self.database.client.delete(self.database.name +"/"+
         util.urlEncode(self.id) + batch, None, headers).getBodyData()

   def copy(self, dest, batch = False, fullCommit = False):
      """
      Copy a document to a destination.

      @param  {str}  dest
      @param  {bool} batch
      @param  {bool} fullCommit
      @return {mixed}
      @raises {Exception}
      """
      if not self.id:
         raise Exception("_id field could not be empty!")

      if not dest:
         raise Exception("Destination could not be empty!")

      batch = "?batch=ok" if batch else ""

      headers = {}
      headers["Destination"] = dest
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"

      return self.database.client.copy(self.database.name +"/"+
         util.urlEncode(self.id) + batch, None, headers).getBodyData()

   def copyFrom(self, dest, batch = False, fullCommit = False):
      """
      Copy a (this) document to a destination with a specific revision.

      @param  {str}  dest
      @param  {bool} batch
      @param  {bool} fullCommit
      @return {mixed}
      @raises {Exception}
      """
      if not self.id or not self.rev:
         raise Exception("Both _id & _rev fields could not be empty!")

      if not dest:
         raise Exception("Destination could not be empty!")

      batch = "?batch=ok" if batch else ""

      headers = {}
      headers["If-Match"] = self.rev
      headers["Destination"] = dest
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"

      return self.database.client.copy(self.database.name +"/"+
         util.urlEncode(self.id) + batch, None, headers).getBodyData()

   def copyTo(self, dest, destRev, batch = False, fullCommit = False):
      """
      Copy a (this) document to an existing document.

      @param  {str}  dest
      @param  {str}  destRev
      @param  {bool} batch
      @param  {bool} fullCommit
      @return {mixed}
      @raises {Exception}
      """
      if not self.id or not self.rev:
         raise Exception("Both _id & _rev fields could not be empty!")

      if not dest or not destRev:
         raise Exception("Destination & destination revision could not be empty!")

      batch = "?batch=ok" if batch else ""

      headers = {}
      headers["If-Match"] = self.rev
      headers["Destination"] = "%s?rev=%s" % (dest, destRev)
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"

      return self.database.client.copy(self.database.name +"/"+
         util.urlEncode(self.id) + batch, None, headers).getBodyData()

