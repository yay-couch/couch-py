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
