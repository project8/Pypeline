# standard libs
import sys
from uuid import uuid4
# custom
from pypeline import DripInterface
from power_spectrum import power_spectrum


def sweep_spectrum():
    '''
    sweep_spectrum is a function that sets some digitization parameters for the
    sweeper, and then hands things off to power_spectrum.

        Arguments:
        -h   ->   Prints this help message
        -p   ->   Enter sweeper power in dBm
        -start -> Enter start frequency in MHz
        -stop  -> Enter stop frequency in MHz
        -t   ->   Enter sweep time in milliseconds

        Arguments for power_spectrum may also be passed to sweep_spectrum, and
        the help file for that function follows below.
    '''
    drip = DripInterface('http://p8portal.phys.washington.edu:5984')

    if '-h' in sys.argv:
        print(sweep_spectrum.__doc__)
    if '-p' in sys.argv:
        power = sys.argv[sys.argv.index('-p') + 1]
        drip.Set('hf_sweeper_power', power)
    if '-start' in sys.argv:
        start = sys.argv[sys.argv.index('-start') + 1]
        drip.Set('hf_sweep_start', start)
    if '-stop' in sys.argv:
        stop = sys.argv[sys.argv.index('-stop') + 1]
        drip.Set('hf_sweep_stop', stop)
    if '-t' in sys.argv:
        time = sys.argv[sys.argv.index('-time') + 1]
        drip.Set('hf_sweep_time', time)

    power_spectrum(args=sys.argv, subprocess='sweepline')

if __name__ == '__main__':
    sweep_spectrum()
