class Couch():
   config = {}
   def __init__(self, config={}, debug=False):
      config["debug"] = debug
      self.setConfig(config)

   def setConfig(self, config={}):
      if config:
         for i in config:
            self.config[i] = config[i]

   def getConfig(self):
      return self.config

Couch.NAME = "Couch"
Couch.VERSION = "1.0.0"
Couch.DEBUG = False
