from distutils.core import setup

verstr = "none"
try:
    verstr = open("VERSION").read().strip().replace(' ','.')
except EnvironmentError:
    pass #There is no file version file
except:
    raise RuntimeError("unable to find version")

setup(
    name = 'Pypeline',
    version = verstr,
    packages = ['pypeline','pypeline/scripts','pypeline/scripts/dpph', 'pypeline/scripts/take_data', 'pid_control', 'pype_logger'],
    scripts = ['gpypeline']
)
