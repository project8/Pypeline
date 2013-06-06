'''
    Class specifically for interactions with the sensor dump database
'''

# standard imports
from datetime import datetime
# 3rd party imports
# local imports
from .SensorDumpDocument import SensorDumpDocument


class _SensorDumpInterface:
    '''
        Class for interactions with the sensor dump database.

        This class is meant to be internal to pypeline and should
        NOT be used directly.
    '''

    def __init__(self, sensor_dump_database):
        '''
            <sensor_dump_database> is the sensor dump database
                                   (element of a couchdb Sever object)
        '''
        self._sensor_dump_database = sensor_dump_database
        #debugging things
        import couchdb
        svr = couchdb.Server('http://localhost:5984')
        self._sensor_dump_database = svr['sensor_dump_debug']
        self._formatstr = '%Y-%m-%d %H:%M:%S'

    def _NewDump(self, doc_id, run_tag='', new_run=False):
        '''
        '''
        runs = {}
        runcount = self._sensor_dump_database.view('runs/sequence_count',
                                                  group_level=2)
        for run in runcount:
            print('run is:')
            print(run)
            runs[run['key']] = {'sequence_count': run['value']}
        runinfo = self._sensor_dump_database.view('runs/run_info',
                                                  group_level=2)
        for run in runinfo:
            runs[run['key']]['run_number'] = run['value']['run_number']
            runs[run['key']]['run_timestamp'] = run['value']['run_timestamp']

        dump_doc = {'run_tag': run_tag,
                    'timestamp': datetime.now().strftime(self._formatstr)
                   }
        if not run_tag in runs and new_run:
            print('creating new run')
            dump_doc['run_number'] = len(runcount)
            dump_doc['run_timestamp'] = datetime.now()
            dump_doc['sequence_number'] = 0
            dump_doc['sequence_tag'] = ''
        elif run_tag in runs and not new_run:
            print('adding to existing run')
            dump_doc['run_number'] = runs[run_tag]['run_number']
            dump_doc['run_timestamp'] = runs[run_tag]['run_timestamp']
            dump_doc['sequence_number'] = run[run_tag]['sequence_count']
            dump_doc['sequence_tag'] = ''
        elif (run_tag in runs and new_run):
            raise RunTagNotUnique('tag already exists')
        elif (not run_tag in runs and not new_run):
            raise ValueError('tag does not exist')
        if dump_doc:
            return_doc = SensorDumpDocument(self._sensor_dump_database, doc_id)
            return_doc.update(dump_doc)
            return_doc._UpdateTo()
        else:
            return_doc = None
        return return_doc
