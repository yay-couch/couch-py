import pprint

def pre(x):
   pprint.pprint(x)

def prd(x, all=False):
   name = "%s" % (x)
   name = name[1:name.find(" ")]
   for attr in dir(x):
      # show only attrs
      if all == False and attr[:2] != "__":
         print "<%s>.%s = %s" % (name, attr, getattr(x, attr))
      elif all == True:
         print "<%s>.%s = %s" % (name, attr, getattr(x, attr))

