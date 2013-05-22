'''
    Class specifically for interactions with the pypeline configuration database
'''

# standard imports
# 3rd party imports
# local imports
try:
    from .DripResponse import DripResponse
except ImportError:
    from DripResponse import DripResponse


class _PypeConfInterface:
    '''
        Class for interactions with the pypeline configurations database.

        This class is meant to be internal to pypeline and should NOT be used directly.
    '''

    def __init__(self, pype_conf_database):
        '''
            <pype_conf_database> is the pypeline configuration database (element of a couchdb Server object)
        '''
        self._pype_conf_db = pype_conf_database

    def ListWithProperty(self, property_name):
        '''
            Return a list of channels with property_name in the document's property field
        '''
        return_list = []
        for row in self._pype_conf_db.view('channel_lists/all'):
            if property_name in self._pype_conf_db[row['id']]['properties']:
                return_list.append(row['key'])
        return return_list

    def ChannelInfo(self, channel_name):
        '''
            Return the description field for <channel_name>
        '''
        return_str = "Channel " + channel_name + " not found"
        for row in self._pype_conf_db.view('channel_list/all'):
            if row['key'] is channel_name:
                try:
                    return_str = self._pype_conf_db[row['id']]['description']
                except KeyError as e:
                    if e[0] is 'description':
                        return_str = "channel has no description string, consider adding one"
                    else:
                        raise
        return return_str
