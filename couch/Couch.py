class Couch():
   config = {}
   def __init__(self, config={}, debug=False):
      if "debug" not in config:
         config["debug"] = debug
      Couch.DEBUG = config["debug"]
      self.setConfig(config)

   def setConfig(self, config={}):
      if config:
         for i in config:
            self.config[i] = config[i]

   def getConfig(self):
      return self.config

Couch.NAME = "Couch"
Couch.VERSION = "1.0.0"
