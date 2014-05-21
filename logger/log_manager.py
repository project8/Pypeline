'''
'''

# standard libs
from multiprocessing import Pool
from uuid import uuid4
# local libs
from pypeline import DripInterface
from .logger import logger

class log_manager:
    '''
    '''

    def __init__(self, dripline_db_url):
        '''
        '''
        self.db_url = dripline_db_url
        self.loggers = {}
        self.pool = False

    def __call__(self):
        '''
        '''
        self.ConfFromDatabase()
        self.StartLoggers()
        return self

    def ConfFromDatabase(self):
        '''
        '''
        db_logger_rows = DripInterface(self.db_url).LoggerConfigurations()
        for logger in db_logger_rows:
            self.AddLogger(logger['key'], logger['value']['channel'], float(logger['value']['interval']))

    def AddLogger(self, logger_key, channel, interval):
        '''
        '''
        if logger_key in self.loggers.keys():
            logger_key += "_" + uuid4().hex
        self.loggers[logger_key] = {"pype_url":self.db_url,
                                    "channel":channel,
                                    "interval":interval,
                                    "start":True}

    def RemoveLogger(self, logger_key):
        '''
        '''
        self.loggers.pop(logger_key)

    def StartLoggers(self):
        '''
        '''
        self.StopLoggers()
        self.pool = Pool(processes=len(self.loggers))
        self.pool.map_async(_StartLogger, self.loggers.values())
        #self.pool.map(_StartLogger, self.loggers.values())
    
    def StopLoggers(self):
        '''
        '''
        if self.pool:
            self.pool.terminate()
            self.pool = False

def _StartLogger(kwargs_dict):
    l = logger(**kwargs_dict)
    l()
