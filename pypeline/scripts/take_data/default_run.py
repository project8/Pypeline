def Mantis_kwargs():
    '''
        Return a dict of kwargs for DripInterface.RunMantis()
    '''
    kwargs = {
        'output': '/data/temp.egg',
        'rate': 250.,
        'duration': 60000.,
        'mode': 1,
        'length': 2097152,
        'count': 640,
        'description': '{}'
    }
    return kwargs


def DefaultParams():
    '''
        Return a list of tuples of the form (channel_name, value).

        These will all be set once before the run starts.
    '''
    defaults = [
        ('trap_current', 0),
        ('dpph_current', 0),
        ('waveguide_cell_heater_current', 0)
    ]
    return defaults


def SequenceParams(sequence_number):
    '''
        Return a list of tuples for a particular sequence number
    '''
    params = []
    if sequence_number % 3 == 0:
        params.append(('trap_current', -1))
    elif sequence_number % 3 == 1:
        params.append(('trap_current', 0))
    elif sequence_number % 3 == 2:
        params.append(('trap_current', 1))
    else:
        raise ValueError("catchall case shouldn't be reached")
    return params


def FilenamePrefix(sequence_number):
    '''
        Return the string filename prefix for a particular sequence.
        Does NOT inlcude the run number or sequence number
    '''
    prefix = datetime.now().strftime("%B%Y")
    if (sequence_number % 3 == 0):
        prefix += 'anti'
    elif (sequence_number % 3 == 1):
        prefix += 'off'
    elif (sequence_number % 3 == 2):
        prefix += 'on'
    else:
        raise ValueError("that's... not possible")
    return prefix
