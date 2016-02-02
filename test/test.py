import couch as _couch
# import couch.util.Util as util
from couch.util.Util import *

couch = _couch.Couch({},  True)
client = _couch.Client(couch)

# client.get("/?a=1")

# print(client.getRequest().toString())
# print(client.getResponse().toString())

# response = client.get("/?a=1")
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
# print server.getActiveTasks()
# print server.getAllDatabases()
# print server.getDatabaseUpdates()
# print server.getLogs()
# print server.getStats()
# print server.getStats("couchdb/uuid")
# print server.getUuid()
# print server.getUuids(3)
# print server.replicate({"source":"foo", "target":"foo_replica", "create_target":True})
# print server.restart()
# print server.getConfig()
# print server.getConfig("couchdb")
# print server.getConfig("couchdb", "uuid")
# print server.setConfig("couchdb", "foo", "the foo!")
# print server.removeConfig("couchdb", "foo")

database = _couch.Database(client, "foo")
# print database.ping()
# print database.info()
# print database.create()
# print database.remove()
# print database.replicate("foo_py")
# print database.getDocument("0f1eb3ba90772b64aee2f44b3c00055b")
# print database.getDocumentAll()
# print database.getDocumentAll({"limit":1})
# print database.getDocumentAll({}, ["0f1eb3ba90772b64aee2f44b3c00055b"])
