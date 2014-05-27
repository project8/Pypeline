'''
'''
from __future__ import print_function, absolute_import
# standard libs
from multiprocessing import Pool, Process
from uuid import uuid4
import logging
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
        self.process_list = []

    def __call__(self):
        '''
        '''
        self.ConfFromDatabase()
        self.StartLoggers()
        return self

    def ConfFromDatabase(self):
        '''
        '''
        self.loggers = {}
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
        self.process_list = [Process(target=logger, kwargs=kwargs) for kwargs in self.loggers.values()]
        for p in self.process_list:
            p.start()
    
    def StopLoggers(self):
        '''
        '''
        if self.process_list:
            for p in self.process_list:
                p.terminate()
            self.process_list = []

    def Update(self):
        '''
        '''
        self.ConfFromDatabase()
        self.StartLoggers()
