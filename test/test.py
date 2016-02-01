import couch as _couch
# import couch.util.Util as util
from couch.util.Util import *

couch = _couch.Couch({}, True)
client = _couch.Client(couch)

# client.get("/?a=1")

# print(client.getRequest().toString())
# print(client.getResponse().toString())

response = client.get("/?a=1")
# print response.getBody()
# print response.getBodyData()
# print response.getBodyData("uuid")
# print response.getBodyData()["uuid"]
# print response.getBodyData("vendor.version")

server = _couch.Server(client)
# print server.ping()
# print server.info()
# print server.info("vendor.name")
# print server.version()
