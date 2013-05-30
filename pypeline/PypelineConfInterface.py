'''
    Class specifically for interactions with the pypeline configuration database
'''

# standard imports
# 3rd party imports
from couchdb.mapping import Document, TextField, ListField
# local imports


class _PypelineConfInterface:
    '''
        Class for interactions with the pypeline configurations database.

        This class is meant to be internal to pypeline and should NOT be used directly.
    '''

    def __init__(self, pype_conf_database):
        '''
            <pype_conf_database> is the pypeline configuration database (element of a couchdb Server object)
        '''
        self._pype_conf_db = pype_conf_database

    def GetChannelDoc(self, channel):
        '''
            Return the couch doc with configurations for channel <channel>
        '''
        result = None
        channels = self._pype_conf_db.view('channel_lists/all')
        ids = [row['id'] for row in channels.rows if row['key'] == channel]
        if len(ids) == 1:
            result = self._pype_conf_db[ids[0]]
        return result

    def UpdateChannel(self, channel, update_dict):
        '''
        '''
        ch_doc = self.GetChannelDoc(channel)
        ch_doc.update(update_dict)
        ch_doc.store(self._pype_conf_db)

    # ListOfChannels and ListWithProperty should be one method with optional arugments
    def ListOfChannels(self):
        '''
        '''
        return [row['key'] for row in self._pype_conf_db.view('channel_lists/all')]

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
        for row in self._pype_conf_db.view('channel_lists/all'):
            if row['key'] == channel_name:
                try:
                    return_str = self._pype_conf_db[row['id']]['description']
                except KeyError as e:
                    if e[0] is 'description':
                        return_str = "channel has no description string, consider adding one"
                    else:
                        raise
        return return_str
