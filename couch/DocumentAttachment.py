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

   def setDocument(self, document):
      if not isinstance(document, couch.Document):
         raise Exception("'document' arg must be instance of couch.Document")
      super.__setattr__(self, "document", document)

   def getDocument(self):
      return self.document
