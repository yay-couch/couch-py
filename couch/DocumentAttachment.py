import couch
import couch.util.Util as util

from os.path import basename

class DocumentAttachment(object):
   document = None
   file, fileName = None, None
   data, dataLength = None, 0
   contentType = None
   digest = None

   def __init__(self, document = None, file = None, fileName = None):
      if document:
         self.setDocument(document)
      if file:
         self.file = file
         self.fileName = fileName if fileName else basename(file)

   def __setattr__(self, name, value):
      if not hasattr(self, name):
         raise Exception("`%s` property does not exists on this object!" % name)
      if name == "file":
         super.__setattr__(self, "file", value)
         super.__setattr__(self, "fileName", basename(value))
      else:
         super.__setattr__(self, name, value)

   def __getattr__(self, name):
      if not hasattr(self, name):
         raise Exception("`%s` property does not exists on this object!" % name)
      return super.__getattr__(self, name)

   def setDocument(self, document):
      if not isinstance(document, couch.Document):
         raise Exception("'document' arg must be instance of couch.Document")
      super.__setattr__(self, "document", document)

   def getDocument(self):
      return self.document

   def ping(self, *args):
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
      headers["Accept"] = "*/*"
      headers["Content-Type"] = None
      if self.digest:
         headers["If-None-Match"] = '"%s"' % (self.digest)
      database = self.document.getDatabase()
      response = database.client.get("%s/%s/%s" %
         (database.name, util.urlEncode(docId), util.urlEncode(self.fileName)), query, headers)
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
