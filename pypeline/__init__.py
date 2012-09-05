'''
    pypeline is the user scripting and interactive interface for the dripline slow control system.

    There is currently support for use with both python 2.7 and python 3.2 (earlier probably works also).
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
    if environ["DISPLAY"]:
        try:
            from .peakdet import peakdet
        except ImportError:
            try:
                from peakdet import peakdet
            except ImportError:
                print('import of peakdet failed, some dependency must be missing')
        try:
            from .LoggedDataHandler import LoggedDataHandler
        except ImportError:
            try:
                from LoggedDataHandler import LoggedDataHandler
            except ImportError:
                print('import of LoggedDataHandler failed, it is not available')
