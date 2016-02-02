import couch
import couch.util.Util as util

class Database():
   client = None
   name = None
   def __init__(self, client, name):
      if not isinstance(client, couch.Client):
         raise Exception("'client' arg must be instance of couch.Client")
      self.client = client
      self.name = name

   def ping(self):
      return (200 == self.client.head(self.name).getStatusCode())

   def info(self, key=None):
      return self.client.get(self.name).getBodyData(key)

   def create(self):
      return (True == self.client.put(self.name).getBodyData("ok"))

   def remove(self):
      return (True == self.client.delete(self.name).getBodyData("ok"))

   def replicate(self, target, targetCreate=True):
      return self.client.post("/_replicate", None, {
         "source"       : self.name,
         "target"       : target,
         "create_target": targetCreate,
      }).getBodyData()

   def getDocument(self, key):
      data = self.client.get(self.name +"/_all_docs", {
         "include_docs": True,
         "key"         : "\"%s\"" % util.quote(key),
      }).getBodyData()
      try:
         return data["rows"][0]
      except: pass

   def getDocumentAll(self, query={}, keys=[]):
      if "include_docs" not in query:
         query["include_docs"] = True
      if not keys:
         return self.client.get(self.name +"/_all_docs", query)
      return self.client.post(self.name +"/_all_docs", query, {"keys": keys}).getBodyData()

   def createDocument(self, document):
      data = self.createDocumentAll([document])
      try:
         return data[0]
      except: pass

   def createDocumentAll(self, documents):
      docs = []
      for document in documents:
         if isinstance(document, couch.Document):
            document = document.getData()
         # this is create method, no update allowed
         if "_rev" in document:     del document["_rev"]
         if "_deleted" in document: del document["_deleted"]
         docs.append(document)
      return self.client.post(self.name +"/_bulk_docs", None, {"docs": docs}).getBodyData()

   def updateDocumentAll(self, documents):
      docs = []
      for document in documents:
         if isinstance(document, couch.Document):
            document = document.getData()
         if "_id" not in document or "_rev" not in document:
            raise Exception("Both _id & _rev fields are required!")
         docs.append(document)
         return self.client.post(self.name +"/_bulk_docs", None, {"docs": docs}).getBodyData()
