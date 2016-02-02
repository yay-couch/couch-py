class Server():
   client = None
   def __init__(self, client):
      self.client = client

   def ping(self):
      return (200 == self.client.head("/").getStatusCode())

   def info(self, key=None):
      return self.client.get("/").getBodyData(key)

   def version(self):
      return self.info("version")

   def getActiveTasks(self):
      return self.client.get("/_active_tasks").getBodyData()

   def getAllDatabases(self):
      return self.client.get("/_all_dbs").getBodyData()

   def getDatabaseUpdates(self, query=None):
      return self.client.get("/_db_updates", query).getBodyData()

   def getLogs(self, query=None):
      return self.client.get("/_log", query, {
         "Content-Type": None,
         "Accept": "text/plain",
      }).getBody()

   def getStats(self, path=""):
      return self.client.get("/_stats/"+ path).getBodyData()

   def getUuid(self, count=1):
      uuids = self.getUuids(1)
      if len(uuids):
         return uuids[0]

   def getUuids(self, count=1):
      return self.client.get("/_uuids/", {"count": count}).getBodyData("uuids")

   def replicate(self, query={}):
      if "source" not in query or "target" not in query:
         raise Exception("Both source & target required!")
      return self.client.post("/_replicate", None, query).getBodyData()

   def restart(self):
      return (202 == self.client.post("/_restart").getStatusCode())

   def getConfig(self, section="", key=""):
      path = "%s/%s" % (section, key)
      return self.client.get("/_config/"+ path).getBodyData()

