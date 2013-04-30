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
try:
    from .dpph_lockin import dpph_lockin
except ImportError:
    from dpph_lockin import dpph_lockin
try:
    import scripts
except ImportError:
    #from scripts import *
    print('crap')
    raise
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
        try:
            from .LoggedDataHandler_Gnuplot import LoggedDataHandler_Gnuplot
        except ImportError:
            try:
                from LoggedDataHandler_Gnuplot import LoggedDataHandler_Gnuplot
            except ImportError:
                print('import of LoggedDataHandler failed, it is not available')
        try:
            from .PlotMakingGui import PlotMakingGui
        except ImportError:
            try:
                from PlotMakingGui import PlotMakingGui
            except ImportError:
                print('import of PlotMakingGui failed, it is not available')
        try:
            from .PlotMakingGui import start_plotgui
        except ImportError:
            try:
                from PlotMakingGui import start_plotgui
            except ImportError:
                print('import of PlotMakingGui failed, it is not available')
        try:
            from .usegnuplot import Gnuplot
        except ImportError:
            try:
                from usegnuplot import Gnuplot
            except ImportError:
                print('import of Gnuplot failed, it is not available')
