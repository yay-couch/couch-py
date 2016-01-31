import couch as _couch
# import couch.util.Util as util
from couch.util.Util import *

couch = _couch.Couch()
client = _couch.Client(couch)
request = _couch.http.Request(client)
request.setMethod("GET")
# prd(request)

# res = request.send()
# print res

res = client.request("GET /?a=1")
pre(res)
