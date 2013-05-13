# Standard
# 3rd Party
from numpy import arange
# Local



def compression_test(pype, power_start=-80, power_stop=-10, power_step=5,
                     sweep_frequency= 25500, lo_frequency=50,
                     digitization_time=10):
    '''
        Execute a compression test

        Inputs:
            <pype>: pypeline.DripInterface instance
            <power_start>: low power for scan (in dBm)
            <power_stop>: high power for scan (in dBm)
            <power_step>: power step size (in dBm)
            <sweep_frequency>: sweeper frequency(in MHz)
            <lo_frequency>: frequency at which to scan (in MHz)
            <digitization_time>: duration of mantis run (in ms)
    '''
    pype.Set('hf_cw_freq', sweep_frequency)
    pype.Set('lo_cw_freq', lo_frequency)
    tempfile = '/data/thisisatempfileforcompressiontests.egg'
    powers = []
    for power in arange(power_start, power_stop, power_step):
        pype.Set('hf_sweeper_power', power)
        run_out = pype.Run(filename=tempfile, durration=digitization_time)
        #something to run powerline and get the power back
        #further processing of powerline output
        #something to append the power list

    #something to plot the two sets of data

