# Standard
# 3rd Party
from numpy import arange
# Local


def transfer_function_2nd_stage(pype, lo_start_freq, lo_stop_freq, lo_step,
                                source_power, channel, dig_time=1000):
    '''
        Measure the transfer function of the low frequency receiver stage

        Inputs:
            <pype>: pypeline.DripInterface instance
            <lo_start_freq>: local oscillator scan start frequency (MHz)
            <lo_stop_freq>: local oscillator scan stop frequency (MHz)
            <lo_step>: local oscillator scan step size (MHz)
            <source_power>: power of the noise source used (?????)
            <channel>: channel to do the scan on
            <dig_time>: duration of mantis run in ms
    '''


    for lo_val in arange(lo_start_freq, lo_stop_freq, lo_step):
        pype.Set('lo_cw_freq', lo_val)
        pype.Run(duration=dig_time)
        #more powerline steps to get the powers
    #plot power of each channel against lo freq and/or save as locust_mc .json input
