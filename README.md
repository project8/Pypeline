Pypeline
========

A python interface for the dripline slow control system.

The goal of pypeline is to create a simple, python based, interface to the dripline slow control system. A single class should wrap the entire couchDB interface and support connections to katydid based analysis. A collection of run scripts, developed for Project 8, will also be included.

Development is being done in python 2.7, hopefully support for python 3 will be added soon.

Dependencies
------------
couchdb-python:
    
    1) for python 2.x I'm using: [couchdb-python](http://code.google.com/p/couchdb-python)
    2) for python 3.x I'm using the port: [couchdb-python3](https://github.com/lilydjwg/couchdb-python3)

Development Notes
-----------------
As in katydid, I'll follow the branching model found here (http://nvie.com/posts/a-successful-git-branching-model/)

Coding standards will follow PEP8 (http://www.python.org/dev/peps/pep-0008/)
