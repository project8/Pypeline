Pypeline
========

A python interface for the dripline slow control system.

The goal of pypeline is to create a simple, python based, interface to the dripline slow control system. A single class should wrap the entire couchDB interface and support connections to katydid based analysis. A collection of run scripts, developed for Project 8, will also be included.

Development is being done using python 2.7 and 3.2 on MacOS 10.7 or later and gentoo linux (kernel 3.3.8). Debugging and testing often uses ipython for both python 2 and python 3.

Dependencies
------------
Where possible, the same codebase will be used for dependencies in python 2 as in python 3.

couchdb-python:

    1) I'm (Ben) running couchdb-python3 (http://github.com/lilydjwg/couchdb-python3) it is a fork from (http://code.google.com/p/couchdb-python) with a patch for python3 support. Note that the origin branch is the original python2 source which I'm using for python2. I'm using the current HEAD for python3. I've forked the repo into http://github.com/laroque/couchdb-python3 incase lilydjwg decides to take it down, I don't currently plan to modify anything.
    1) for python 2.x I'm using: [couchdb-python](http://code.google.com/p/couchdb-python)
    2) for python 3.x I'm using the port: [couchdb-python3](https://github.com/lilydjwg/couchdb-python3)


matplotlib:

    1) I'm (Micah) using version 1.2.x. Find it at http://matplotlib.sourceforge.net/.
    2) I'm (Ben) using version 1.2.x from http://github.com/matplotlib/matplotlib


numpy:

    1) I'm (Micah) using version 1.5.1 Find it at http://numpy.scipy.org/
    2) I'm (Ben) using version 1.7.x from http://github.com/numpy/numpy

scipy:

    1) I'm (Micah) using 0.12.0.dev-8647010. Find it at http://numpy.scipy.org.
    2) I'm (Ben) using 0.12.x from http://github.com/scipy/scipy


Development Notes
-----------------
As in katydid, I'll follow the branching model found here (http://nvie.com/posts/a-successful-git-branching-model/)

Coding standards will follow PEP8 (http://www.python.org/dev/peps/pep-0008/)
