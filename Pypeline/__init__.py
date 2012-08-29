'''
    Package init for pypeline. For now pypeline.py containing the pypeline class is all there is so not much here.
'''
from os import environ

try:
    from .DripInterface import DripInterface
except ImportError:
    import DripInterface.DripInterface
try:
    from .DripResponse import DripResponse
except ImportError:
    from DripResponse import DripResponse
if "DISPLAY" in environ:
    if environ["Display"]:
        try:
            from . import peakdet
        except ImportError:
            try:
                from peakdet import peakdet
            except ImportError:
                print('import of peakdet failed, some dependency must be missing')
        try:
            from . import LoggedDataHandler
        except ImportError:
            try:
                from LoggedDataHandler import LoggedDataHandler
            except ImportError:
                print('import of LoggedDataHandler failed, it is not available')
