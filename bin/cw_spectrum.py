# standard libs
import sys
from uuid import uuid4
# custom
from pypeline import DripInterface
from power_spectrum import power_spectrum


def cw_spectrum():
    '''
    cw_spectrum is a function that sets some digitization parameters, and then
    hands things off to power_spectrum.

        Arguments:
        -h  -> Print this help message
        -p  -> Enter high-frequency power in dBm
        -hf -> Enter high-frequency cw frequency in MHz

        Arguments for power_spectrum may also be passed to cw_spectrum, and the
        help file for that function follows below.
    '''
    drip = DripInterface('http://p8portal.phys.washington.edu:5984')
    if '-h' in sys.argv:
        print(cw_spectrum.__doc__)
    if '-p' in sys.argv:
        power = sys.argv[sys.argv.index('-p') + 1]
        drip.Set('hf_sweeper_power', power)
    if '-hf' in sys.argv:
        hf = sys.argv[sys.argv.index('-hf') + 1]
        drip.Set('hf_cw_freq', hf)

    power_spectrum(args=sys.argv)

if __name__ == '__main__':
    cw_spectrum()
