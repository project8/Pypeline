from __future__ import print_function, absolute_import
# standard libs
from Tkinter import (Button, Label, Entry,
                     StringVar, BooleanVar, IntVar)
from tkFileDialog import askopenfilename
from time import sleep
import multiprocessing
import sys
import imp
from uuid import uuid4
# 3rd party libs
# local libs
from ...PypelineErrors import NoResponseError


class take_data:
    '''
    '''

    def __init__(self, pype, toplevel):
        '''
        '''
        self.pype = pype
        self.toplevel = toplevel

        self.keep_runningVar = BooleanVar(value=True)
        self.run_tagVar = StringVar()
        self.numSequencesVar = IntVar(value=10)
        self.params = {}
        self.runthread = multiprocessing.Process()

        self._GetParamFuncs(filename=False)
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

        Label(self.toplevel, text='Load Custom Run Def').grid(row=row,
                                                              column=0)
        Button(self.toplevel, text="find file", command=self._ParamFuncFile
               ).grid(row=row, column=1)
        row += 1

        Button(self.toplevel, text="Start Run", command=self.DoRun
               ).grid(row=row, column=0)
        Button(self.toplevel, text="ABORT", command=self._Abort, bg='red'
               ).grid(row=row, column=1)
        Button(self.toplevel, text="Is Running?", command=self._IsRunning
               ).grid(row=row, column=2)

    def _ParamFuncFile(self):
        '''
        '''
        filename = askopenfilename()
        if filename:
            self._GetParamFuncs(filename)

    def _Abort(self):
        '''
        '''
        self.keep_runningVar.set(False)
        if self.runthread.is_alive():
            print('terminating child process')
            self.runthread.terminate()
        else:
            print('no current thread')

    def _IsRunning(self):
        '''
        '''
        print(self.runthread.is_alive())

    def _GetParamFuncs(self, filename=False):
        '''
        '''
        if not filename:
            if not 'run_params' in sys.modules:
                #imp.load_module('run_params', None
                #import .default_run as run_params
                from . import default_run as run_params
        Button(self.toplevel, text="Start Run", command=self.DoRun
               ).grid(row=row, column=0)
        Button(self.toplevel, text="ABORT", command=self._Abort, bg='red'
               ).grid(row=row, column=1)
        Button(self.toplevel, text="Is Running??", command=self._IsRunning
               ).grid(row=row, column=2)

    def _Abort(self):
        '''
        '''
        self.keep_runningVar.set(False)
        if self.runthread.is_alive():
            print('terminating child process')
            self.runthread.terminate()
        else:
            print('no current thread')

    def _IsRunning(self):
        '''
        '''
        print(self.runthread.is_alive())

    def _GetParamFuncs(self, filename=False):
        '''
        '''
        if not filename:
            if not 'run_params' in sys.modules:
                #imp.load_module('run_params', None
                #import .default_run as run_params
                from . import default_run as run_params
            else:
                reload(run_params)
        else:
            imp.load_source('run_params', filename)
            import run_params
        self.DefaultParams = run_params.DefaultParams
        self.SequenceParams = run_params.SequenceParams

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
        self._SetParams(self.DefaultParams())
        print('defaults should be set now')
        for sequence_num in range(self.params['num_sequences']):
            if not self.keep_runningVar.get():
                print('Aborting!')
                break
            self._DoSequence(sequence_num)
        print('run sequence aborted or completed')

    def _SetParams(self, params_list):
        '''
        '''
        for channel_name, value in params_list:
            #if self.pype.Set(channel_name, value).Wait().Waiting():
            #    raise NoResponseError('setting ' + str(channel_name))
            print('*'*60, '\nskipping Set() calls while debugging')
            print(channel_name, '->', value)


    def _DoSequence(self, sequence_number):
        '''
            Do one sequence within the run
        '''
        print('*'*60, '\nsequence is:', sequence_number)
        run_doc = self.pype._NewDump(uuid4().hex, self.params['run_tag'],
                                new_run=(not sequence_number))
        self._SetParams(self.SequenceParams(sequence_number))
        print('*'*60, '\nnow trying to get dump channels')
        for channel in self.pype.ListWithProperty('dump'):
            print('*'*60, '\nnow for channel', channel)
            run_doc[channel] = self.pype.Get(channel)
            print('get submitted')
            run_doc[channel].Update()
            print('updated')
            run_doc[channel].Wait()
            print('waited')
        run_doc._UpdateTo()
        trap_status = ''
        if (sequence_number % 3 == 0):
            trap_status = 'anti'
        elif (sequence_number % 3 == 1):
            trap_status = 'off'
        elif (sequence_number % 3 == 2):
            trap_status = 'on'
        else:
            print('got to else', sequence_number % 3)
            raise ValueError("that's... not possible")
        outfilename = '/data/june2013_{:s}_{:05d}_{:05d}.egg'.format(
            trap_status, run_doc['run_number'], run_doc['sequence_number'])
        run_descrip = ''
        run = self.pype.RunMantis(output=outfilename, mode=1, description=run_descrip,
                                  duration=60000)
        sleep(60)
        run.Wait()
        run_doc['mantis'] = run
        run_doc._UpdateTo()
        print('actually, nothing yet')
