import couch
from couch.util.Util import *

client = couch.Client()
request = couch.http.Request(client)
request.setMethod("GET")
# prd(request)

res = request.send()
pre(res)
