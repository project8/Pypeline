#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from os import environ

setup(name="PyplineExtend",
    ext_modules=[
        Extension("PowerSpectrum", ["PowerSpectrumModule.cpp"],
            libraries = ["boost_python-mt"],
            include_dirs = filter(None, environ['CPLUS_INCLUDE_PATH'].split(':')) +
                [environ['ROOTSYS']+'/include'],
            library_dirs = filter(None, environ['LD_LIBRARY_PATH'].split(':')) +
                [environ['ROOTSYS']+'/lib'])
    ])
