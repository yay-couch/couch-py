import pprint

def pre(o):
   pprint.pprint(o)

def prd(o, all=False):
   name = getObjectName(o)
   for attr in dir(o):
      # show only attrs
      if all == False and attr[:2] != "__":
         print "<%s>.%s = %s" % (name, attr, getattr(o, attr))
      elif all == True:
         print "<%s>.%s = %s" % (name, attr, getattr(o, attr))

def getObjectName(o):
   name = "%s" % (o)
   name = name[1:name.find(" ")]
   return name
