Pypeline
========

A python interface for the dripline slow control system.

The goal of pypeline is to create a simple, python based, interface to the dripline slow control system. A single class should wrap the entire couchDB interface and support connections to katydid based analysis. A collection of run scripts, developed for Project 8, will also be included.

I hope to maintain compatibility with both python 2.7 and python 3.2 or greater but that may be dropped in the interest of quick development, at least initially. A couchDB library for python will be a required dependency but hopefully not much else.

Dependencies
------------
couchdb-python:
    
    1) for python 2.x I'm using: [couchdb-python](http://code.google.com/p/couchdb-python)
    2) for python 3.x I'm using the port: [couchdb-python3](https://github.com/lilydjwg/couchdb-python3)