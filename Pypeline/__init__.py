'''
    Package init for pypeline. For now pypeline.py containing the pypeline class is all there is so not much here.
'''

from DripInterface import DripInterface
from DripResponse import DripResponse
try:
    from peakdet import peakdet
except ImportError:
    print('import of peakdet failed, some dependency must be missing')
try:
    from LoggedDataHandler import LoggedDataHandler
except ImportError:
    print('import of LoggedDataHandler failed, it is not available')
