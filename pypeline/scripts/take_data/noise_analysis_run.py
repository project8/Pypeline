from datetime import datetime


def Mantis_kwargs():
    '''
        Return a dict of kwargs for DripInterface.RunMantis()
    '''
    kwargs = {
        'output': '/data/temp.egg',
        'rate': 500.,
        'duration': 1000.,
        'mode': 1,
        'length': 2097152,
        'count': 128,
        'description': '{}'
    }
    return kwargs


def DefaultParams():
    '''
        Return a list of tuples of the form (channel_name, value).

        These will all be set once before the run starts.
    '''
    defaults = []
    return defaults


def SequenceParams(sequence_number):
    '''
        Return a list of tuples for a particular sequence number
    '''
    params = []
    return params


def FilenamePrefix(sequence_number):
    '''
        Return the string filename prefix for a particular sequence.
        Does NOT inlcude the run number or sequence number
    '''
    prefix = datetime.now().strftime("%B%Y")
    return prefix
