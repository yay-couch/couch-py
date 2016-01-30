import pprint

def pre(x):
   pprint.pprint(x)

def prd(obj):
   for attr in dir(obj):
      print ">> obj.%s = %s" % (attr, getattr(obj, attr))
