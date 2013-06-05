from __future__ import print_function, absolute_import
# standard libs
from Tkinter import (Button, Label, Entry,
                     StringVar, BooleanVar, IntVar)
from time import sleep
import multiprocessing
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
        self.numSequencesVar = IntVar(value=100)
        self.params = {}
        self.runthread = multiprocessing.Process()

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

        Label(self.toplevel, text='Number of Sequences').grid(row=row,
                                                              column=0)
        Entry(self.toplevel, textvariable=self.numSequencesVar).grid(row=row,
                                                                     column=1)
        row += 1

        Button(self.toplevel, text="Start Run", command=self.DoRun
               ).grid(row=row, column=0)
        Button(self.toplevel, text="ABORT", command=self._Abort, bg='red'
               ).grid(row=row, column=1)
        Button(self.toplevel, text="Is Running?", command=self._IsRunning
               ).grid(row=row, column=2)

    def _Abort(self):
        '''
        '''
        self.keep_runningVar.set(False)
        print(self.runthread.is_alive())
        self.runthread.terminate()

    def _IsRunning(self):
        '''
        '''
        print(self.runthread.is_alive())

    def DoRun(self):
        '''
            Execute the run
        '''
        self.keep_runningVar.set(True)
        if self.runthread.is_alive():
            print('there is already live process, abort first or let it finish')
        else:
            self.runthread = multiprocessing.Process(target=self._DoRun)
            self.runthread.start()

    def _DoRun(self):
        '''
        '''
        self.params['run_tag'] = self.run_tagVar.get()
        self.params['num_sequences'] = self.numSequencesVar.get()
        for sequence_num in range(self.params['num_sequences']):
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
        print('tag is:', self.params['run_tag'])
        print('though you currently think it is:', self.run_tagVar.get())
        print('sequence is:', sequence_num)
        sleep(5)
        print('actually, nothing yet')
