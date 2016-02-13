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
# default=localhost
config.host = "couchdb_host"
# default=5984
config.port = 1234
# default=null
config.username = "couchdb_user"
# default=null
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
couch = new Couch.Couch()

# init couch object with given config
couch = new Couch.Couch(config, debug)

# or set later but before streaming
couch = new Couch.Couch()
couch.setConfig(config, debug)
```
