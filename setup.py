from setuptools import setup
from glob import glob

verstr = "none"
try:
    verstr = open("VERSION").read().strip().replace(' ','.')
    open("pypeline/__version.py", mode="w").write("'''This file generated automatically'''\n\n__version__ = '" + verstr + "'")
except EnvironmentError:
    pass #There is no file version file
except:
    raise RuntimeError("unable to find version")

setup(
    name = 'Pypeline',
    version = verstr,
    packages = ['pypeline','pypeline/scripts','pypeline/scripts/dpph', 'pypeline/scripts/take_data', 'pid_control', 'pype_logger'],
    scripts = glob('*/bin/*') + glob('bin/*')
)
