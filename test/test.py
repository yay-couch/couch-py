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

database = _couch.Database(client, "foo_py")
# print database.ping()
# print database.info()
# print database.create()
# print database.remove()
# print database.replicate("foo_py")
# print database.getDocument("0f1eb3ba90772b64aee2f44b3c00055b")
# print database.getDocumentAll()
# print database.getDocumentAll({"limit":1})
# print database.getDocumentAll({}, ["0f1eb3ba90772b64aee2f44b3c00055b"])
# document = _couch.Document()
# print database.createDocumentAll([document])
# print database.createDocument({"title":"The Book 1", "price":1.5})
# print database.createDocumentAll([{"title":"The Book 1", "price":1.5}])
# print database.updateDocument({"title":"The Book 1.1", "price":1.5,
#    "_id":"83b921545793787b051dd356410014c2", "_rev":"2-dc87c52dcb43ae2449b9a8070229b2ce"})
# print database.updateDocumentAll([{"title":"The Book 1.1", "price":1.5,
   # "_id":"83b921545793787b051dd356410014c2", "_rev":"1-d8dbc8aba800e04fa1d90059df208bbb"}])
# print database.deleteDocument({"_id":"83b921545793787b051dd356410014c2", "_rev":"3-839b4a1b168b742015f97adff9e24100"})
# print database.deleteDocumentAll([{"_id":"83b921545793787b051dd356410014c2", "_rev":"3-839b4a1b168b742015f97adff9e24100"}])
# print database.getChanges({"limit":1})
# print database.getChanges({}, ["7ee9cdd673b109e030cec8c6f10105bc"])
# print database.compact()
# print database.ensureFullCommit()
# print database.viewCleanup()
# print database.viewTemp("function(doc){if(doc.name) emit(doc,null)}")
# print database.getSecurity()
# print database.setSecurity()
# print database.getMissingRevisions("7ee9cdd673b109e030cec8c6f10105bc", ["3-839b4a1b168b742015f97adff9e24100"])
# print database.getMissingRevisionsDiff("7ee9cdd673b109e030cec8c6f10105bc", ["3-839b4a1b168b742015f97adff9e24100"])
# print database.getRevisionLimit()
# print database.setRevisionLimit(1001)

doc = _couch.Document(database)
doc._id = "0f1eb3ba90772b64aee2f44b3c00055b"
# doc._rev = "1-3c92d3e67136c8b206d90ea37a3ee76d"
# doc.type = "py_test"
# prd(doc)

# print doc.ping()
# print doc.isExists()
# print doc.isNotModified()
# print doc.find()
# print doc.findRevisions()
# print doc.findRevisionsExtended()
# print doc.findAttachments()
# print doc.findAttachments(True, ["1-3c92d3e67136c8b206d90ea37a3ee76d"])
# print doc.save()
# doc._id = "0f1eb3ba90772b64aee2f44b3c00055b_copy"
# doc._rev = "2-79bfd93b5daabe1581a962a0fe89426f"
# doc.type = "py_test"
# print doc.remove()
# print doc.copy("0f1eb3ba90772b64aee2f44b3c00055b_copy_2")

docAttc = _couch.DocumentAttachment(doc)
docAttc.file = __file__
prd(docAttc)

# print _couch.Uuid.generate(_couch.Uuid.TIMESTAMP)
# print _couch.Uuid.generate(_couch.Uuid.HEX_8)
# print _couch.Uuid.generate(_couch.Uuid.HEX_32)
# print _couch.Uuid.generate(_couch.Uuid.HEX_40)
