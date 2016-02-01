class Server():
   client = None
   def __init__(self, client):
      self.client = client

   def ping(self):
      return (200 == self.client.head("/").getStatusCode())
