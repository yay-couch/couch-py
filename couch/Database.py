class Database():
   client = None
   name = None
   def __init__(self, client, name):
      self.client = client
      self.name = name
