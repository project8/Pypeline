'''
    Source for the _CmdInterface class, actual content which interacts with
    the dripline_cmd database.
'''
from __future__ import print_function, absolute_import

# standard imports
from time import sleep
from uuid import uuid4

# 3rd party imports

# local imports
try:
    from .DripResponse import DripResponse
except ImportError:
    from DripResponse import DripResponse


class _CmdInterface:

    '''
        Internal:
            This class is meant to be internal to pypeline (DripInterface
            primarily) and should NOT be used directly by the user. If you feel
            compelled to use it directly then DripInterface probably needs some
            new features.

        Class which actually interacts with the dripline_cmd database.
            Primarily this means it contains properly formatted documents to be
            filled in and posted. Most of the methods here will have a
            counterpart in DripInterface by the same name which is the primary
            place where they are called.
    '''

    def __init__(self, cmd_database):
        '''
            Inputs:
                <cmd_database> is the dripline command database
                               (element of a couchdb Server object)
        '''
        self._cmd_database = cmd_database

    def _Get(self, channel):
        '''
            Post a "get" document to the command database.

            Inputs:
                <channel> must be an active channel in dripline.

            Returns:
                a DripResponse instance.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        get_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "get",
                "channel": channel,
            },
        }
        self._cmd_database.save(get_doc)
        return result

    def _GetFromSet(self, channel):
        '''
        '''
        vw = self._cmd_database.view('latest_set/pure_setters', group_level=2)
        doc_id = [row['value']['_id'] for row in vw if row['key']==channel][0]
        result = DripResponse(self._cmd_database, doc_id)
        result.Update()
        return result

    def _Set(self, channel, value):
        '''
            Post a "set" document to the command database

            Inputs:
                <channel> must be an active channel in dripline
                <value> value to assign to <channel>

            Returns:
                a DripResponse instance
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        set_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "set",
                "channel": channel,
                "value": str(value),
            },
        }
        self._cmd_database.save(set_doc)
        return result

    def _StartLoggers(self, instruments):
        '''
            Posts a "syscmd" document to start one ore more loggers

            Inputs:
                <instruments> instrument name or list of names.

            Returns:
                A DripResponse instance.
        '''
        if isinstance(instruments, str):
            instruments = [instruments]
        result = DripResponse(self._cmd_database, uuid4().hex)
        start_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "syscmd",
                "action": "start_loggers",
                "args": instruments,
            },
        }
        self._cmd_database.save(start_doc)
        return result

    def GetPureSetters(self):
        '''
        '''
        pure_setters = []
        setters_view = self._cmd_database.view('latest_set/pure_setters', group_level=2)
        for row in setters_view:
            pure_setters.append(row['key'])
        return pure_setters

    def StopLoggers(self, instruments):
        '''
            Posts a "syscmd" document to stop one or more loggers

            Inputs:
                <instruments> instrument name or list of names

            Returns:
                a DripResponse instance
        '''
        if instruments == 'all':
            instruments = self.CurrentLoggers().Wait()['final']
        if isinstance(instruments, str):
            instruments = [instruments]
        result = DripResponse(self._cmd_database, uuid4().hex)
        stop_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "syscmd",
                "action": "stop_loggers",
                "args": instruments,
            },
        }
        self._cmd_database.save(stop_doc)
        return result

    def CurrentLoggers(self):
        '''
            Tells the dripline logger to list which instruments are currently
            being logged.

            Returns:
                A DripResponse instance
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        start_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "syscmd",
                "action": "current_loggers",
            },
        }
        self._cmd_database.save(start_doc)
        return result

    def RunMantis(self, output, rate, duration, mode, length, count,
                  description):
        '''
            Take a digitizer run of fixed time and sample rate.

            Inputs:
                <output> the output file to which we should write
                <rate> digitization rate in MHz
                <duration> duration in ms
                <mode> channel mode to use (1 or 2)
                <length> length of record to use in bytes
                <count> number of circular buffer nodes to use
                <description> string description

            Returns:
                A DripResponse instance
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        run_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "run",
                "subprocess": "mantis",
                "output": output,
                "rate": str(rate),
                "duration": str(duration),
                "mode": str(mode),
                "length": str(length),
                "count": str(count),
                "description": str(description)
            },
        }
        self._cmd_database.save(run_doc)
        return result

    def RunPowerline(self, points, events, input_file):
        '''
            Posts a "run" document calling a non-mantis process

            Inputs:
                <points> number of fft points to use
                <event> max number of records to use
                <input_file> input file to process

            Returns:
                A DripResponse instance.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        run_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "run",
                "subprocess": "powerline",
                "points": str(points),
                "events": str(events),
                "input": input_file
            },
        }
        self._cmd_database.save(run_doc)
        return result

    def RunSweepline(self, points, events, input_file):
        '''
            Posts a "run" document calling a non-mantis process

            Inputs:
                <points> number of fft points to use
                <event> max number of records to use
                <input_file> input file to process

            Returns:
                A DripResponse instance.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        run_doc = {
            '_id': result['_id'],
            'type': 'command',
            'command': {
                "do": "run",
                "subprocess": "sweepline",
                "points": str(points),
                "events": str(events),
                "input": input_file
            },
        }
        self._cmd_database.save(run_doc)
        return result
