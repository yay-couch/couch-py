import re

from Stream import Stream

class Response(Stream):
   status = None
   statusCode = 0
   statusText = ""
   def __init__(self):
      self.type = Stream.TYPE["RESPONSE"];
      self.httpVersion = "1.0";

   def setStatus(self, status):
      r = re.match("^HTTP/(\d+\.\d+)\s+(\d+)\s+(.+)", status)
      if not r:
         return
      self.status = status.strip()
      m = r.groups()
      if len(m) == 3:
         self.httpVersion = m[0]
         self.setStatusCode(m[1])
         self.setStatusText(m[2])

   def setStatusCode(self, statusCode):
      self.statusCode = int(statusCode)

   def setStatusText(self, statusText):
      self.statusText = statusText.strip()

   def getStatus(self):
      return self.status

   def getStatusCode(self):
      return self.statusCode

   def getStatusText(self):
      return self.statusText

   def setBody(self, body):
      if body != None:
         self.body = body

Response.STATUS = {
   200: "OK",
   201: "Created",
   202: "Accepted",
   304: "Not Modified",
   400: "Bad Request",
   401: "Unauthorized",
   403: "Forbidden",
   404: "Not Found",
   405: "Resource Not Allowed",
   406: "Not Acceptable",
   409: "Conflict",
   412: "Precondition Failed",
   415: "Bad Content Type",
   416: "Requested Range Not Satisfiable",
   417: "Expectation Failed",
   500: "Internal Server Error",
}
