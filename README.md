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
config["host"] = "couchdb_host"
# default=5984
config["port"] = 1234
# default=""
config["username"] = "couchdb_user"
# default=""
config["password"] = "************"

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
   "create_target": True})

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
doc._id = "abc"
doc._rev = "3-abc"
# param as Couch.Document
db.updateDocument(doc)
# param as dict
db.updateDocument({
    "_id": "abc",
   "_rev": "1-abc",
   "test": "test (update)"
})

# delete a document
doc = Couch.Document(None, {
    "_id": "abc",
   "_rev": "1-abc",
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
doc._id = "abc"
doc._rev = "2-abc"

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
doc.setAttachment({"file": "./file.txt"}) # name goes to be file.txt
doc.setAttachment({"file": "./file.txt", "file_name": "my_file_name"})
doc.setAttachment(Couch.DocumentAttachment(doc, file, fileName=None))
doc.save()
```

### DocumentAttachment Object

```python
attc = Couch.DocumentAttachment(doc)

# ping attachment
attc.ping()

# find an attachment
attc.fileName = "my_attc_name"
attc.find()

# find an attachment by digest
attc.fileName = "my_attc_name"
attc.digest   = "U1p5BLvdnOZVRyR6YrXBoQ=="
attc.find()

# add an attachment to document
attc.file     = "attc.txt"
attc.fileName = "my_attc_name"
attc.save()

# remove an attachment from document
attc.fileName = "my_attc_name"
attc.remove()

# to json/array
attc.toJson()
attc.toArray()
```

### DocumentDesign Object

```python
# @todo
```

## Uuid

```python
# create uuid given value
uuid = Couch.Uuid("my_uuid")
# auto-generate using os.urandom() => 32 length hexed
uuid = Couch.Uuid(True)

# also setValue & getValue methods available
uuid = Couch.Uuid()
uuid.setValue("my_uuid")

# print
print uuid.toString()

# generate method (default=HEX_32)
uuidValue = Couch.Uuid.generate(limit)
uuidValue = Couch.Uuid.generate(Couch.Uuid.HEX_40)

# available limits
HEX_8     = 8
HEX_32    = 32
HEX_40    = 40
TIMESTAMP = 0
```

## Query

```python
# init query
query = Couch.Query()
# init query with data (params)
query = Couch.Query({"foo": 1})

# add params
query.set("conflicts", True) \
   .set("stale", "ok") \
   .skip(1) \
   .limit(2)

# get as string
print query.toString()

# use it!
db.getDocumentAll(query)
```

## Request / Response

```python
# after any http stream (server ping, database ping, document save etc)
client.request("GET /")

# dump raw stream with headers/body parts
print client.getRequest().toString()
print client.getResponse().toString()

# get response body (string)
print client.getResponse().getBody()

# get response data (parsed)
print client.getResponse().getBodyData()
# >> {u'version': u'14.04', u'name': u'Ubuntu'}
print client.getResponse().getBodyData("vendor")
# >> Ubuntu
print client.getResponse().getBodyData("vendor.name")

"""
GET / HTTP/1.1
Host: localhost:5984
Connection: close
Accept: application/json
Content-Type: application/json
User-Agent: Couch/v1.0.0 (+http://github.com/yay-couch/couch-py)


HTTP/1.1 200 OK
Server: CouchDB/1.5.0 (Erlang OTP/R16B03)
Date: Fri, 13 Nov 2015 02:45:12 GMT
Content-Type: application/json
Content-Length: 127
Cache-Control: must-revalidate

{"couchdb":"Welcome","uuid":"5a660f4695a5fa9ab2cd22722bc01e96", ...
"""
```

## Error Handling

Couch will not throw any server response error, such as `409 Conflict` etc. It only throws library-related errors or wrong usages of the library (ie. when `_id` is required for some action but you did not provide it).

```python
# create issue
doc = Couch.Document()
doc._id = "an_existing_docid"

# no error will be thrown
doc.save()

# but could be so
if 201 != client.getResponse().getStatusCode():
   print "nö!"

   # or show response error string
   print client.getResponse().getError()

   # or show response error data
   data = client.Response().getErrorData()
   print data["error"]
   print data["reason"]
```
