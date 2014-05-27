'''
    The pypeline logger will duplicate the functionality of the integrated dripline logger.  It is meant to serve as an alternative for instances when the loggers are broken. It could also be useful for things that need to be logged but which are not actual dripline channels.
'''
from __future__ import print_function, absolute_import
# system libraries
from time import sleep
import logging
# custom libs
from pypeline import DripInterface

class logger:
    '''
        The logger class does simple, brute force, logging. When started it will log one channel and a prescribed interval indefinately.
    '''

    def __init__(self, **kwargs):
        logging.info('initializing a logger')
        if kwargs:
            self.SetupChannel(**kwargs)
        if 'start' in kwargs:
            if kwargs['start']:
                self.__call__()

    def __call__(self, **kwargs):
        logging.info('starting a logger loop')
        self.StartLogLoop()

    def SetupChannel(self, **kwargs):
        '''
            Configure this logger with a pypeline DripInterface instance, channel, etc. For now, the only supported logging mode is a dripline channel which supports a "get" verb. This could be expanded in the future if deemed useful. This is probably where this should happen.

            Inputs:
                valid kwargs are:
                    pype_url -> a url for a DripInterface instance __init__
                    channel -> name of the channel to log
                    interval -> approximate time between logging of values [seconds]
        '''
        valid_kwargs = {'pype_url', 'channel', 'interval', 'start'}
        if kwargs and not set(kwargs.keys()).issubset(valid_kwargs):
            raise KeyError('invalid keyword arugment')
        for kwarg in kwargs:
            if kwarg == 'start':
                continue
            if kwarg == 'pype_url':
                self.pype = DripInterface(kwargs[kwarg])
                continue
            setattr(self, kwarg, kwargs[kwarg])

    def StartLogLoop(self):
        '''
            Begin continuous logging. This is a blocking function call.
        '''
        while True:
            self._LogChannel()
            sleep(self.interval)
    
    def _LogChannel(self):
        '''
            so here, self.pype.Get could be changed to self.AcquireMethod which is part of the configuration, it could then log non-dripline things, if that is useful.
        '''
        get_result = self.pype.Get(self.channel).Wait()
        logging.info('logging %s', self.channel)
        log = {'sensor':self.channel,
               'uncal_val':str(get_result.Result()),
               'cal_val':str(get_result.Final()),
               'timestamp':str(get_result.TimeStamp()),}
        self.pype.LogValue(**log)
