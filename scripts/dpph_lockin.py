from pypeline import DripInterface, scripts
from sys import argv

if not len(argv) == 2:
    print('usage: $ python dpph_lockin.py guess')
    print('where guess is the frequency to start near')
pype = DripInterface('http://p8portal.phys.washington.edu:5984')
scripts.dpph_lockin(pype, float(argv[1]))
