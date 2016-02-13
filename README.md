## Couch

Simply port of [Couch](https://github.com/yay-couch/couch) library for Python.

Notice: See CouchDB's official documents before using this library.

## In a Nutshell

```python
# create a fresh document
doc = Couch.Document(db)
doc.name = "The Doc!"
doc.save()

# append an attachment to the same document above
doc.setAttachment(Couch.DocumentAttachment(doc, "./file.txt"))
doc.save()
```

## Install

```shell
git clone git@github.com:yay-couch/couch-py.git && cd couch-py && python setup.py install
```

## Configuration

Configuration is optional but you can provide all these options;

```python
config = {}
# default="localhost"
config.host = "couchdb_host"
# default=5984
config.port = 1234
# default=""
config.username = "couchdb_user"
# default=""
config.password = "************"

# this will dump whole request/response messages for each stream
# default=False
debug = True
```

## Objects

### Couch Object

```python
# get the big boy!
import couch as Couch

# init couch object with default config
couch = Couch.Couch()

# init couch object with given config
couch = Couch.Couch(config, debug)

# or set later but before streaming
couch = Couch.Couch()
couch.setConfig(config, debug)
```

### Client Object

```python
# used in Server and Database objects
client = Couch.Client(couch)
```

If you need any direct request for any reason, you can use the methods below.
```python
print client.request("GET /")

# shortcut methods that handle HEAD, GET, POST, PUT, COPY, DELETE
# without body
client.head(uri, uriParams={}, headers={})
client.get(uri, uriParams={}, headers={})
client.copy(uri, uriParams={}, headers={})
client.delete(uri, uriParams={}, headers={})
# with body
client.put(uri, uriParams={}, body=None, headers={})
client.post(uri, uriParams={}, body=None, headers={})

# after request operations
# request = client.getRequest()
# response = client.getResponse()
```

### Server Object

```python
server = Couch.Server(client)

# methods
server.ping()
server.info(key="")
server.version()

server.getActiveTasks()
server.getAllDatabases()
server.getDatabaseUpdates(query)
server.getLogs(query)

server.restart()
server.replicate(query={"source": "foo", "target": "foo2",
   "create_target": true})

server.getStats(path="")
server.getStats("/couchdb/request_time")

server.getUuid()   # get one
server.getUuids(3) # get three

server.getConfig(section, key)
server.getConfig("couchdb")
server.getConfig("couchdb", "uuid")
server.setConfig("couchdb", "foo", "the foo!")
server.removeConfig("couchdb", "foo")
```

### Database Object

```python
db = Couch.Database(client, "foo")

# db methods
db.ping()
db.info(key="")
db.create()
db.remove()
db.replicate(target, targetCreate=True)
db.getChanges(query={}, docIds=[])
db.compact(ddoc="")
db.ensureFullCommit()
db.viewCleanup()
db.getSecurity()
db.setSecurity(admins={}, members={})

db.getRevisionLimit()
db.setRevisionLimit(limit)


# tmp view method
db.viewTemp(map="", reduce="")

# document methods
db.purge(docId="", docRevs=[])
db.getMissingRevisions(docId="", docRevs=[])
db.getMissingRevisionsDiff(docId="", docRevs=[])
# get a document
db.getDocument(key="")
# get all documents
db.getDocumentAll(query={}, keys=[])

# create a document
doc = Couch.Document()
doc.name = "test"
# param as Couch.Document
db.createDocument(doc)
# param as object
db.createDocument({"name": "test"})

# update a document
doc = Couch.Document()
doc._id = "e90636c398458a9d5969d2e71b04ad81"
doc._rev = "3-9aeefae43b9fad5df8cc87fe8bcc2718"
# param as Couch.Document
db.updateDocument(doc)
# param as dict
db.updateDocument({
    "_id": "e90636c398458a9d5969d2e71b04b0a4",
   "_rev": "1-afa338dcbc6870f1a1dd441557f79859",
   "test": "test (update)"
})

# delete a document
doc = Couch.Document(None, {
    "_id": "e90636c398458a9d5969d2e71b04b0a4",
   "_rev": "1-afa338dcbc6870f1a1dd441557f79859",
})
db.deleteDocument(doc)

# multiple CRUD
docs = []

# all accepted, just fill the doc data
docs.append({
   # doc data id etc (and rev for updade/delete)
})
docs.append(Couch.Document(None, {
   # doc data id etc (and rev for updade/delete)
}))
doc = Couch.Document()
doc.foo = "..."
docs.append(doc)

# multiple create
db.createDocumentAll(docs)
# multiple update
db.updateDocumentAll(docs)
# multiple delete
db.deleteDocumentAll(docs)
```

### Document Object

```python
doc = Couch.Document(db)
# set props (so data)
doc._id = "e90636c398458a9d5969d2e71b04b2e4"
doc._rev = "2-393dbbc2cca7eea546a3c750ebeddd70"

# checker method
doc.ping(callback)

# CRUD methods
doc.find(query={})
doc.remove(batch=False, fullCommit=False)
# create
doc.save(batch=False, fullCommit=False)
# update
doc._id = "abc"
doc._rev = "1-abc"
doc.save(batch=False, fullCommit=False)

# copy methods
doc.copy(dest, batch=False, fullCommit=False)
doc.copyFrom(dest, batch=False, fullCommit=False)
doc.copyTo(dest, destRev, batch=False, fullCommit=False)

# find revisions
doc.findRevisions()
doc.findRevisionsExtended()

# find attachments
doc.findAttachments(attEncInfo=False, attsSince=[])

# add attachments
doc.setAttachment({"file": "./file.txt"}); # name goes to be file.txt
doc.setAttachment({"file": "./file.txt", "file_name": "my_file_name"})
doc.setAttachment(Couch.DocumentAttachment(doc, file, fileName=None))
doc.save()
```
