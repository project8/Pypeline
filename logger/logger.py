'''
    The pypeline logger will duplicate the functionality of the integrated dripline logger.  It is meant to serve as an alternative for instances when the loggers are broken. It could also be useful for things that need to be logged but which are not actual dripline channels.
'''

from time import sleep

class logger:
    '''
        The logger class does simple, brute force, logging. When started it will log one channel and a prescribed interval indefinately.
    '''

    def __init__(self, **kwargs):
        if kwargs:
            self.SetupChannel(**kwargs)
        if 'start' in kwargs:
            if kwargs['start']:
                self.__call__()

    def __call__(self, **kwargs):
        self.StartLogLoop()

    def SetupChannel(self, **kwargs):
        '''
            Configure this logger with a pypeline DripInterface instance, channel, etc. For now, the only supported logging mode is a dripline channel which supports a "get" verb. This could be expanded in the future if deemed useful. This is probably where this should happen.

            Inputs:
                valid kwargs are:
                    pype -> a DripInterface instance, used for 'getting'
                    channel -> name of the channel to log
                    interval -> approximate time between logging of values [seconds]
        '''
        valid_kwargs = {'pype', 'channel', 'interval', 'start'}
        if kwargs and not set(kwargs.keys()).issubset(valid_kwargs):
            raise KeyError('invalid keyword arugment')
        for kwarg in kwargs:
            if kwarg == 'start':
                continue
            setattr(self, kwarg, kwargs[kwarg])

    def StartLogLoop(self):
        '''
            Begin continuous logging. This is a blocking function call.
        '''
        while True:
            print('log again')
            self._LogChannel()
            sleep(self.interval)
    
    def _LogChannel(self):
        '''
            so here, self.pype.Get could be changed to self.AcquireMethod which is part of the configuration, it could then log non-dripline things, if that is useful.
        '''
        get_result = self.pype.Get(self.channel).Wait()
        log = {'sensor':self.channel,
               'uncal_val':get_result.Result(),
               'cal_val':get_result.Final(),
               'timestamp':get_result.TimeStamp(),}
        self.pype.LogValue(**log)
