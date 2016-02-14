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

class Database():
   """
   Database object.

   @module couch
   @object couch.Database
   @author Kerem Güneş <k-gun@mail.com>
   """

   # Client object.
   # @var couch.Client
   client = None

   # Database name.
   name = None

   def __init__(self, client, name):
      """
      Object constructor.

      @param  {couch.Client} client
      @param  {str}          name
      @raises {Exception}
      """
      if not isinstance(client, couch.Client):
         raise Exception("'client' arg must be instance of couch.Client")

      self.client = client
      self.name = name

   def ping(self):
      """
      Ping database, expect 200 response code.

      @return {bool}
      """
      return (200 == self.client.head(self.name).getStatusCode())

   def info(self, key = None):
      """
      Get database info.

      @param  {str|None} key
      @return {mixed}
      """
      return self.client.get(self.name).getBodyData(key)

   def create(self):
      """
      Create a new database.

      @return {bool}
      """
      return (True == self.client.put(self.name).getBodyData("ok"))

   def remove(self):
      """
      Remove database.

      @return {bool}
      """
      return (True == self.client.delete(self.name).getBodyData("ok"))

   def replicate(self, target, targetCreate = True):
      """
      Replicate database.

      @param  {str}  target
      @param  {bool} targetCreate
      @return {mixed}
      """
      return self.client.post("/_replicate", None, {
         "source"       : self.name,
         "target"       : target,
         "create_target": targetCreate,
      }).getBodyData()

   def getDocument(self, key):
      """
      Get a document by given key (docid).

      @param  {str} key
      @return {mixed}
      """
      data = self.client.get(self.name +"/_all_docs", {
         "include_docs": True,
         "key"         : "\"%s\"" % util.quote(key),
      }).getBodyData()

      try:
         return data["rows"][0]
      except: pass

   def getDocumentAll(self, query = {}, keys = []):
      """
      Get all documents by given query options. If keys params provided, request for
      documents by given keys.

      @param  {dict} query
      @param  {list}  keys
      @return {mixed}
      """
      query = query or {}
      if "include_docs" not in query:
         query["include_docs"] = True

      if not keys:
         return self.client.get(self.name +"/_all_docs", query)
      else:
         return self.client.post(self.name +"/_all_docs", query,
            {"keys": keys}).getBodyData()

   def createDocument(self, document):
      """
      Create a document.

      @param  {mixed} document
      @return {mixed|None}
      """
      data = self.createDocumentAll([document])
      try:
         return data[0]
      except: pass

   def createDocumentAll(self, documents):
      """
      Create multiple documents.

      @param  {list} documents
      @return {mixed}
      """
      docs = []
      for document in documents:
         if isinstance(document, couch.Document):
            document = document.getData()

         # this is create method, no update allowed
         if "_rev" in document:     del document["_rev"]
         if "_deleted" in document: del document["_deleted"]

         docs.append(document)

      return self.client.post(self.name +"/_bulk_docs", None,
         {"docs": docs}).getBodyData()

   def updateDocument(self, document):
      """
      Update a document.

      @param  {mixed} document
      @return {mixed|None}
      @raises {Exception}
      """
      data = self.updateDocumentAll([document])
      try:
         return data[0]
      except: pass

   def updateDocumentAll(self, documents):
      """
      Update multiple documents.

      @param  {list} documents
      @return {mixed}
      @raises {Exception}
      """
      docs = []
      for document in documents:
         if isinstance(document, couch.Document):
            document = document.getData()

         # these are required params
         if "_id" not in document or "_rev" not in document:
            raise Exception("Both _id & _rev fields are required!")

         docs.append(document)

         return self.client.post(self.name +"/_bulk_docs", None,
            {"docs": docs}).getBodyData()

   def deleteDocument(self, document):
      """
      Delete a document.

      @param  {mixed} document
      @return {mixed|None}
      @raises {Exception}
      """
      data = self.deleteDocumentAll([document])
      try:
         return data[0]
      except: pass

   def deleteDocumentAll(self, documents):
      """
      Delete multiple documents.

      @param  {list} documents
      @return {mixed}
      @raises {Exception}
      """
      docs = []
      for document in documents:
         if isinstance(document, couch.Document):
            document = document.getData()

         # just add "_deleted" param into document
         document["_deleted"] = True

         docs.append(document)

      return self.updateDocumentAll(docs)

   def getChanges(self, query = {}, docIds = []):
      """
      Get database changes.

      @param  {dict|None} query
      @param  {list}      docIds
      @return {mixed}
      """
      if not docIds:
         return self.client.get(self.name +"/_changes", query).getBodyData()

      query = query or {}
      # ensure query filter
      if "filter" not in query:
         query["filter"] = "_doc_ids"

      return self.client.post(self.name +"/_changes", query,
         {"doc_ids": docIds}).getBodyData()

   def compact(self, ddoc = ""):
      """
      Compact database.

      @param  {str} ddoc
      @return mixed
      """
      return self.client.post(self.name +"/_compact/"+ ddoc).getBodyData()

   def ensureFullCommit(self):
      """
      Ensure full-commit.

      @return {mixed}
      """
      return self.client.post(self.name +"/_ensure_full_commit").getBodyData()

   def viewCleanup(self):
      """
      View cleanup, so remove unneded view index files.

      @return {mixed}
      """
      return self.client.post(self.name +"/_view_cleanup").getBodyData()

   def viewTemp(self, map, reduce = None):
      """
      Create (and execute) a temporary view.

      @param  {string}      map
      @param  {string|None} reduce
      @return {mixed}
      """
      return self.client.post(self.name +"/_temp_view", None,
         {"map":map, "reduce":reduce}).getBodyData()

   def getSecurity(self):
      """
      Get the current security object of the database.

      @return {mixed}
      """
      return self.client.get(self.name +"/_security").getBodyData()

   def setSecurity(self, admins = {}, members = {}):
      """
      Set the security object for the database.

      @param  {dict} admins
      @param  {dict} members
      @return {mixed}
      @raises {Exception}
      """
      admins, members = admins or {}, members or {}
      if ("names" not in admins or "roles" not in admins
         or "names" not in members or "roles" not in members):
         raise Exception("Specify admins and/or members with names=>roles fields!")

      return self.client.put(self.name +"/_security", None,
         {"admins":admins, "members":members}).getBodyData()

   def purge(self, docId, docRevs):
      """
      Permanently remove the references to deleted documents from the database.

      @param  {str}  docId
      @param  {list} docRevs
      @return {mixed}
      """
      return self.client.post(self.name +"/_purge", None,
         {docId: docRevs}).getBodyData()

   def getMissingRevisions(self, docId, docRevs):
      """
      Get the document revisions that do not exist in the database.

      @param  {str}  docId
      @param  {list} docRevs
      @return {mixed}
      """
      return self.client.post(self.name +"/_missing_revs", None,
         {docId: docRevs}).getBodyData()

   def getMissingRevisionsDiff(self, docId, docRevs):
      """
      Get the subset of those that do not correspond to revisions stored in the database.

      @param  {str}  docId
      @param  {list} docRevs
      @return {mixed}
      """
      return self.client.post(self.name +"/_revs_diff", None,
         {docId: docRevs}).getBodyData()

   def getRevisionLimit(self):
      """
      Get the current "revs_limit" (revision limit) setting.

      @return {int}
      """
      return self.client.get(self.name +"/_revs_limit").getBodyData()

   def setRevisionLimit(self, limit):
      """
      Set the current "revs_limit" (revision limit) setting.

      @param  {int} limit
      @return {mixed}
      """
      return self.client.put(self.name +"/_revs_limit", None, limit).getBodyData()
