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
# client = new Couch.Client(couch)
```

If you need any direct request for any reason, you can use the methods below.
```python
print client.request("GET /")

# shortcut methods that handle HEAD, GET, POST, PUT, COPY, DELETE
# without body
client.head(uri, uriParams={}, heaaders={})
client.get(uri, uriParams={}, heaaders={})
client.copy(uri, uriParams={}, heaaders={})
client.delete(uri, uriParams={}, heaaders={})
# with body
client.put(uri, uriParams={}, body=None, heaaders={})
client.post(uri, uriParams={}, body=None, heaaders={})

# after request operations
# request  = client.getRequest()
# response = client.getResponse()
```
