# Standard
import ast
# 3rd Party
from numpy import arange
# Local
from ..PypelineErrors import DriplineError


def compression_test(pype, power_start=-80, power_stop=-10, power_step=5,
                     lo_frequency=50, digitization_time=50):
    '''
        Execute a compression test

        Inputs:
            <pype>: pypeline.DripInterface instance
            <power_start>: low power for scan (in dBm)
            <power_stop>: high power for scan (in dBm)
            <power_step>: power step size (in dBm)
            <lo_frequency>: frequency at which to scan (in MHz)
            <digitization_time>: duration of mantis run (in ms)
    '''
    sweep_frequency = lo_frequency + 24250
    pype.Set('hf_cw_freq', sweep_frequency)
    pype.Set('lo_cw_freq', lo_frequency)
    tempfile = '/data/thisisatempfileforcompressiontests.egg'
    descrip = {'lo_frequency': lo_frequency}
    rate = 200
    mode = 1
    power_out = []
    for power in arange(power_start, power_stop, power_step):
        pype.Set('hf_sweeper_power', power)
        mantis_out = pype.RunMantis(filename=tempfile, mode=mode, rate=rate,
                                    durration=digitization_time,
                                    description=descrip)
        mantis_out.Wait(digitization_time/500.)
        if mantis_out.Waiting():
            raise DriplineError('failed to digitize')
        powerline_out = pype.RunPowerline(input_file=tempfile)
        power_out.append(max(ast.literal_eval(powerline_out['final'])['data']))
    result = {'power_in': power, 'power_out': power_out}

    # something to plot the two sets of data
