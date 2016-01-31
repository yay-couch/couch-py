import couch as _couch
# import couch.util.Util as util
from couch.util.Util import *

couch = _couch.Couch()
client = _couch.Client(couch)
# request = _couch.http.Request(client)
# request.setMethod("GET")
# prd(request)

# response = request.send()
# print response

# response = client.head("/?a=1")

client.head("/?a=1")

print
print "---"
print
print(client.getRequest().toString())
print ">>>"
print
print(client.getResponse().toString())
