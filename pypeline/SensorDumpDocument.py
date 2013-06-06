'''
    File to contain the DripResponse class which inherits from dict.
'''

# import standard libraries
from time import sleep
# 3rd party libs
from couchdb.mapping import Document


class SensorDumpDocument(dict):

    '''
        Class which shall be returned by any DripInterface method which
        involves posting a document to a dripline db expecting dripline to
        modify that document.

        This class will handle keeping track of the document's _id,
        and looking for responses stored there by dripline etc.

        Will have a key:value pair for each field of the document.
    '''

    def __init__(self, dump_db, doc_id):
        '''
            Internal: Initializes the default attribute values etc.

            Inputs:
                <cmd_db> the dripline command database. This is where
                         DripResponse will look for updates do documents
                <doc_id> the value of "_id" for the document.
        '''
        dict.__init__(self)
        self._dump_db = dump_db
        self['_id'] = doc_id
        if doc_id in self._dump_db:
            self._UpdateFrom()
        else:
            self._dump_db.save(self)

    def _UpdateFrom(self):
        '''
            Sets a key:value pair for each field of the couch doc.
            Existing key:values are changed and new ones are created.
            Missing keys are NOT removed.

            Changes are made to the current instance but a copy is also
            returned.
        '''
        document = Document.load(self._dump_db, doc_id)
        for field_name in document:
            if not field_name == '_id':
                self[field_name] = document[field_name]

    def _UpdateTo(self):
        '''
            Updates the remote to match local.
        '''
        document = Document.load(self._dump_db, self['_id'])
        if '_rev' in self:
            self.pop('_rev')
        for key in self.keys():
            document[key] = self[key]
        document.store(self._dump_db)
