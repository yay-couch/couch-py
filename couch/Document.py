import couch
import couch.util.Util as util

class Document():
   id, rev = None, None
   deleted = False
   attachments = []
   database = None
   data = {}
   def __init__(self, database=None, data={}):
      if database:
         if not isinstance(database, couch.Database):
            raise Exception("'database' arg must be instance of couch.Database")
         self.database = database
      if data:
         self.data = data

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
