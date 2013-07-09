from __future__ import print_function, absolute_import
from sys import version_info
inpy3 = not version_info[0] < 3

# standard libs
if inpy3:
    from tkinter import (Button, Label, Entry, Checkbutton,
                         StringVar, BooleanVar, IntVar)
    from tkinter.filedialog import askopenfilename
else:
    from Tkinter import (Button, Label, Entry, Checkbutton,
                         StringVar, BooleanVar, IntVar)
    from tkFileDialog import askopenfilename
from time import sleep
import multiprocessing
import sys
import imp
from json import dumps
from uuid import uuid4
import ast
# 3rd party libs
# local libs
from ...PypelineErrors import NoResponseError


class take_data:
    '''
    '''

    def __init__(self, pype, toplevel=False, filename=False, num_sequences=10,
                 run_tag=''):
        '''
        '''
        self.pype = pype
        self.toplevel = toplevel

        self.keep_runningVar = BooleanVar(value=True)
        self.extend_runVar = BooleanVar(value=False)
        self.run_tagVar = StringVar(value=run_tag)
        self.num_sequencesVar = IntVar(value=num_sequences)
        self.stateVar = StringVar(value='done')
        self.params = {}
        self.runthread = multiprocessing.Process()

        self._GetParamFuncs(filename)
        if toplevel:
            self._BuildGui()

    def _BuildGui(self):
        '''
            Setup all of the buttons and user entries
        '''
        row = 0

        Label(self.toplevel, text='Run tag').grid(row=row, column=0)
        Entry(self.toplevel, textvariable=self.run_tagVar).grid(row=row,
                                                                column=1)
        Checkbutton(self.toplevel, text="Extend Existing",
                    variable=self.extend_runVar).grid(row=row, column=2)
        row += 1

        Label(self.toplevel, text='Number of Sequences').grid(row=row,
                                                              column=0)
        Entry(self.toplevel, textvariable=self.num_sequencesVar).grid(row=row,
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
        Label(self.toplevel, textvariable=self.stateVar#, command=self._IsRunning
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
        self.stateVar.set('aborted')

    def _IsRunning(self):
        '''
        '''
        print(self.runthread.is_alive())

    def _Abort(self):
        '''
        '''
        self.keep_runningVar.set(False)
        if self.runthread.is_alive():
            print('terminating child process')
            self.runthread.terminate()
        else:
            print('no current thread')
        self.stateVar.set('aborted')

    def _IsRunning(self):
        '''
        '''
        print(self.runthread.is_alive())

    def _GetParamFuncs(self, filename=False):
        '''
        '''
        if not filename:
            if not 'run_params' in sys.modules:
                from . import default_run as run_params
            else:
                reload(run_params)
        else:
            imp.load_source('run_params', filename)
            import run_params
        self.DefaultParams = run_params.DefaultParams
        self.SequenceParams = run_params.SequenceParams
        self.Mantis_kwargs = run_params.Mantis_kwargs()

    def DoRun(self):
        '''
            Execute the run
        '''
        self.keep_runningVar.set(True)
        self.stateVar.set('normal')
        if self.runthread.is_alive():
            print('there is already live process, abort first or let it finish')
        else:
            self.runthread = multiprocessing.Process(target=self.__DoRun)
            self.runthread.start()

    def __DoRun(self):
        '''
            the run called by DoRun in a subprocess
        '''
        self.params['run_tag'] = self.run_tagVar.get()
        self.params['num_sequences'] = self.num_sequencesVar.get()
        print('setting defaults')
        self._SetParams(self.DefaultParams())
        for sequence_num in range(self.params['num_sequences']):
            print('starting sequence', sequence_num)
            if not self.keep_runningVar.get():
                print('Aborting!')
                break
            self._DoSequence(sequence_num)
        self.stateVar.set('run complete')

    def _SetParams(self, params_list):
        '''
        '''
        print('******** skipping Set() calls while debugging')
        for channel_name, value in params_list:
            if self.pype.Set(channel_name, value).Wait().Waiting():
                raise NoResponseError('setting ' + str(channel_name))
            #print(channel_name, '->', value)

    def _DoSequence(self, sequence_number):
        '''
            Do one sequence within the run
        '''
        mantis_kwargs = self.Mantis_kwargs.copy()
        run_doc = self.pype._NewDump(uuid4().hex, self.params['run_tag'],
                                new_run=((not sequence_number) and 
                                          not self.extend_runVar.get()))
        self._SetParams(self.SequenceParams(sequence_number))
        for channel in self.pype.ListWithProperty('dump'):
            run_doc[channel] = self.pype.Get(channel)
            run_doc[channel].Update()
            run_doc[channel].Wait()
        run_doc._UpdateTo()
        outfilename = '/data/{:s}_{:05d}_{:05d}.egg'.format(
            self.FilenamePrefix(sequence_number),
            run_doc['run_number'],
            run_doc['sequence_number']) 
        run_descrip = ast.literal_eval(mantis_kwargs['description'])
        for (chan,val) in self.SequenceParams(sequence_number):
            run_descrip[chan] = val
        run_descrip['run_tag'] = self.params['run_tag']
        run_doc['sequence_tag'] = dumps(run_descrip)
        mantis_kwargs.update({'output': outfilename,
                              'description':dumps(run_descrip)})
        run = self.pype.RunMantis(*mantis_kwargs)
        print('mantis run starting')
        sleep(60)
        run.Wait()
        run_doc['mantis'] = run
        run_doc._UpdateTo()
