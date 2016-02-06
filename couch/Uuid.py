class Uuid():
   value = None
   def __init__(self, value):
      if value == True:
         value = generate(Uuid.HEX_32)
      self.setValue(value)
