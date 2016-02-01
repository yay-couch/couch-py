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
