import couch
import couch.util.Util as util

class DocumentAttachment(object):
   document = None
   file, fileName = None, None
   data, dataLength = None, 0
   contentType = None
   digest = None

   def __init__(self, document = None, file = None, fileName = None):
      pass

   def setDocument(self, document):
      if not isinstance(document, couch.Document):
         raise Exception("'document' arg must be instance of couch.Document")
      super.__setattr__(self, "document", document)

   def getDocument(self):
      return self.document
