import couch
import couch.util.Util as util

class Document():
   id, rev = None, None
   deleted = False
   attachments = {}
   database = None
   data = {}
   def __init__(self, database=None, data={}):
      if database:
         self.setDatabase(database)
      if data:
         self.setData(data)

   def setDatabase(self, database):
      if not isinstance(database, couch.Database):
         raise Exception("'database' arg must be instance of couch.Database")
      self.database = database

   def geetDatabase(self):
      return self.database

   def setId(self, id):
      if not isinstance(id, couch.Uuid):
         id = couch.Uuid(id)
      self.id = id
   def setRev(self, rev):
      self.rev = rev
   def setDeleted(self, deleted):
      self.deleted = bool(deleted)

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
         self.data['_attachments'][attachment.fileName] = attachment;
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

   def getData(self):
      return {}
