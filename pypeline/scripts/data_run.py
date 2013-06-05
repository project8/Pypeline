from __future__ import print_function, absolute_import
# standard libs
from Tkinter import (Button, Label, Entry, StringVar, BooleanVar)
from time import sleep
import threading
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

        self.keep_runningVar = BooleanVar(value=True)
        self.run_tagVar = StringVar()
        self.run_tag = ''

        self._BuildGui()

    def _BuildGui(self):
        '''
            Setup all of the buttons and user entries
        '''
        row = 0

        Label(self.toplevel, text='Run tag').grid(row=row, column=0)
        Entry(self.toplevel, textvariable=self.run_tagVar).grid(row=row,
                                                                column=1)
        row += 1

        Button(self.toplevel, text="Start Run", command=self.DoRun
               ).grid(row=row, column=0)
        Button(self.toplevel, text="ABORT", command=self._Abort, bg='red'
               ).grid(row=row, column=1)

    def _Abort(self):
        '''
        '''
        self.keep_runningVar.set(False)

    def DoRun(self):
        '''
            Execute the run
        '''
        runthread = threading.Thread(target=self._DoRun)
        runthread.start()

    def _DoRun(self):
        '''
        '''
        self.run_tag = self.run_tagVar.get()
        for sequence_num in range(100):
            if not self.keep_runningVar.get():
                print('Aborting!')
                break
            self._DoSequence(sequence_num)
        print('run sequence aborted or completed')

    def _DoSequence(self, sequence_num):
        '''
            Do one sequence within the run
        '''
        print('doing something...')
        print('tag is:', self.run_tag)
        print('though you currently think it is:', self.run_tagVar.get())
        print('sequence is:', sequence_num)
        sleep(5)
        print('actually, nothing yet')
