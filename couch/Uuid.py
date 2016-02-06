class Uuid():
   value = None
   def __init__(self, value):
      if value == True:
         value = generate(Uuid.HEX_32)
      self.setValue(value)

   def setValue(self, value):
      self.value = value
   def getValue(self):
      return self.value
