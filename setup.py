from distutils.core import setup

setup(
    name = 'Pypeline',
    packages = ['pypeline','pypeline/scripts','pypeline/scripts/dpph', 'pypeline/scripts/take_data', 'pid_control'],
    scripts = ['gpypeline']
)
