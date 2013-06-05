from __future__ import print_function, absolute_import
# standard libs
from Tkinter import (Button, StringVar, BooleanVar)
# 3rd party libs
# local libs

class data_run:
    '''
    '''

    def __init__(self, pype, toplevel):
        '''
        '''
        self.pype = pype
        self.toplevel = toplevel
        self._BuildGui()

        self.keep_runningVar = BooleanVar()

    def _BuildGui(self):
        '''
            Setup all of the buttons and user entries
        '''
        row = 0
        Button(self.toplevel, text="Start Run", command=self.DoRun
               ).grid(row=row, column=0)
        Button(self.toplevel, text="ABORT", command=self._Abort, bg='red'
               ).grid(row=row, column=1)

    def DoRun(self):
        '''
            Execute the run
        '''
        pass

    def _Abort(self):
        '''
        '''
        self.keep_runningVar.set(False)

    def _DoSequence(self):
        '''
            Do one sequence within the run
        '''
        pass
