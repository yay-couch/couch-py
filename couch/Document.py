import couch
import couch.util.Util as util

class Document(object):
   id = None
   rev = None
   deleted = False
   attachments = {}
   database = None
   data = {}
   def __init__(self, database=None, data={}):
      if database:
         self.setDatabase(database)
      if data:
         self.setData(data)
   def __setattr__(self, key, value):
      self.setData({key: value})
   def __getattr__(self, key):
      return self.getData(key)

   def setDatabase(self, database):
      if not isinstance(database, couch.Database):
         raise Exception("'database' arg must be instance of couch.Database")
      super.__setattr__(self, "database", database)

   def getDatabase(self):
      return self.database

   def setId(self, id):
      if not isinstance(id, couch.Uuid):
         id = couch.Uuid(id)
      super.__setattr__(self, "id", id)
   def setRev(self, rev):
      super.__setattr__(self, "rev", rev)
   def setDeleted(self, deleted):
      super.__setattr__(self, "deleted", bool(deleted))

   def getId(self):
      return self.id
   def getRev(self):
      return self.rev
   def getDeleted(self):
      return self.deleted

   def setAttachment(self, attachment):
      if not isinstance(attachment, couch.Attachment):
         if "file" not in attachment:
            raise Exception("Attachment file is required!")
         file = attachment["file"]
         fileName = attachment["file_name"] or None
         attachment = DocumentAttachment(self, file, fileName)
      attcKey = "_attachments."+ attachment.fileName
      if util.isSet(self.data, attcKey):
         raise Exception("Attachment is alredy exists on this document!")
      if "_attachments" not in self.data:
         self.data["_attachments"] = {}
      self.attachments[attachment.fileName] = \
         self.data["_attachments"][attachment.fileName] = attachment

   def getAttachment(self, name):
      if name in self.attachments[name]:
         return self.attachments[name]

   def getAttachmentAll(self):
      return self.attachments

   def unsetAttachment(self, name):
      if name in self.attachments[name]:
         del self.attachments[name]

   def unsetAttachmentAll(self):
      self.attachments = {}

   def setData(self, data={}):
      if "_id" in data: self.setId(data["_id"])
      if "_rev" in data: self.setRev(data["_rev"])
      if "_deleted" in data: self.setDeleted(data["_deleted"])
      if "_attachments" in data:
         for attachment in data["_attachments"]:
            self.setAttachment(attachment)
         del data["_attachments"]
      for key, value in data.items():
         self.data[key] = value

   def getData(self, key = None):
      if key != None:
         return util.dig(key, self.data)
      return self.data

   def ping(self, *args):
      if not self.id:
         raise Exception("_id field is could not be empty!")
      headers = {}
      if self.rev != None:
         headers["If-None-Match"] = '"%s"' % (self.rev)
      response = self.database.client.head(self.database.name +"/"+ util.urlEncode(self.id),
         None, headers)
      responseStatusCode = response.getStatusCode()
      for statusCode in (args or [200]):
         if statusCode == responseStatusCode:
            return True
      return False

   def isExists(self):
      return self.ping(200, 304)

   def isNotModified(self):
      if not self.rev:
         raise Exception("_rev field could not be empty!")
      return self.ping(304)

   def find(self, query = {}):
      if not self.id:
         raise Exception("_id field is could not be empty!")
      query = query or {}
      if "rev" not in query and self.rev:
         query["rev"] = self.rev
      return self.database.client.get(self.database.name +"/"+ util.urlEncode(self.id),
         query).getBodyData()

   def findRevisions(self):
      return util.dig("_revisions", self.find({"revs": True}))

   def findRevisionsExtended(self):
      return util.dig("_revs_info", self.find({"revs_info": True}))

   def findAttachments(self, attEncInfo = False, attsSince = []):
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
      if not self.id:
         # insert action
         ret = self.database.client.post(self.database.name + batch, None,
            data, headers).getBodyData()
         if ret and ("id" in ret):
            self.setId(ret["id"])
      else:
         # update action
         ret = self.database.client.put(self.database.name +"/"+ util.urlEncode(self.id) + batch,
            None, data, headers).getBodyData()
      # for next instant call(s)
      if ret and ("rev" in ret):
         self.setRev(ret["rev"])
      return ret

   def remove(self, batch = False, fullCommit = False):
      if not self.id and not self.rev:
         raise Exception("Both _id & _rev fields could not be empty!")
      batch = "?batch=ok" if batch else ""
      headers = {}
      headers["If-Match"] = self.rev
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"
      return self.database.client.delete(self.database.name +"/"+ util.urlEncode(self.id) + batch,
         None, headers).getBodyData()

   def copy(self, dest, batch = False, fullCommit = False):
      if not self.id:
         raise Exception("_id field could not be empty!")
      if not dest:
         raise Exception("Destination could not be empty!")
      batch = "?batch=ok" if batch else ""
      headers = {}
      headers["Destination"] = dest
      if fullCommit:
         headers["X-Couch-Full-Commit"] = "true"
      return self.database.client.copy(self.database.name +"/"+ util.urlEncode(self.id) + batch,
         None, headers).getBodyData()

   def copyFrom(self, dest, batch = False, fullCommit = False):
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
      return self.database.client.copy(self.database.name +"/"+ util.urlEncode(self.id) + batch,
         None, headers).getBodyData()

   def copyTo(self, dest, destRev, batch = False, fullCommit = False):
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
      return self.database.client.copy(self.database.name +"/"+ util.urlEncode(self.id) + batch,
         None, headers).getBodyData()

