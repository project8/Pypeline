Pypeline
========

A python interface for the dripline slow control system.

The goal of pypeline is to create a simple, python based, interface to the dripline slow control system. A single class should wrap the entire couchDB interface and support connections to katydid based analysis. A collection of run scripts, developed for Project 8, will also be included.

Development is being done using python 2.7 and 3.2 on MacOS 10.7 or later and gentoo linux (kernel 3.3.8). Debugging and testing often uses ipython for both python 2 and python 3.

Getting Started
---------------
The preferred method of installation is with [virtualenv](https://pypi.python.org/pypi/virtualenv). Assuming you have that installed but are otherwise starting from scratch the normal steps are:

```shell
virtualenv --python=python2.7 /path/to/virtualenvironments/pypeline_env
source /path/to/virtualenvironments/pypeline_env/bin/activate
pip install ipython matplotlib scipy CouchDB
git clone git@github.com:project8/Pypeline
cd Pypeline
python setup.py install
deactivate
```

Once complete, you can do: ```source /path/to/virtualenvironments/pypeline_env/bin/activate```. Pypeline should now be ready for use.

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

gnuplot.py: DEPRICATED, gnuplot.py is no longer used
    
    1) I'm (Gray) using 1.8 -BUT NOT ANYMORE-.  Find it at REDACTED
    1b) I'm (Gray) beginning to thing that gnuplot.py was made by a hack.  If it keeps fighting me I'm going to write my own version.
    1c) I (Gray) have affirmed gnuplot.py is a piece of junk and have replaced it with my own code

tkinter:
    The tell me (Gray) that it comes with all python distributions.  I'm using v2.7.3
    *for portage users, be sure to have +tk on python (off by default)

pmw: DEPRICATED? this is likely not to be used, that may change
    I'm (Gray)  using version 1.3.2a
    *it seems the newer 2.0.0 version has issues depending on your version of tkinter

Development Notes
-----------------
As in katydid, I'll follow the branching model found here (http://nvie.com/posts/a-successful-git-branching-model/)

Coding standards will follow PEP8 (http://www.python.org/dev/peps/pep-0008/)
