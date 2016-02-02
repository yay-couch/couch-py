class Database():
   client = None
   name = None
   def __init__(self, client, name):
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
