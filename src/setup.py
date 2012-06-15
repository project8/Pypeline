#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from os import environ

setup(name="PyplineExtend",
    ext_modules=[
        Extension("PowerSpectrum", ["PowerSpectrumModule.cpp"],
            libraries = ["boost_python-mt"],
            library_dirs = filter(None, environdict['LD_LIBRARY_PATH'].split(':')))
    ])
