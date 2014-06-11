#!/usr/bin/python

from __future__ import print_function

import pypeline
import subprocess
import json
import sys

frequencies = range(400, 1401, 10)
frequencies = [500, 520]

#def Digitize(filename, lo):
#    temp_conf = open("full_spectrum_mantis_temp.json", "w")
#    subprocess.call(['sed', 's/FILENAME/{:s}/'.format(filename), 'full_spectrum_mantis_template.json'], stdout=temp_conf)
#    temp_conf.close()
#    subprocess.call(['sed', '-i', 's/LOFREQ/%i/'%lo, 'full_spectrum_mantis_temp.json'])
#    subprocess.call(['cat full_spectrum_mantis_temp.json | ssh ignatius "cat > temp.json"'], shell=True)
#    subprocess.call(['ssh','ignatius','/usr/local/bin/mantis_client','config=~/temp.json'])

def full_spectrum(config):
    '''
    '''
    lo_pype = pypeline.DripInterface(config.pop('lo_pype'))
    trap_pype = pypeline.DripInterface(config.pop('trap_pype'))
    file_prefix = config.pop('data_prefix')
    mantis_kwargs = {"description": "full_spectrum, automatic run"}
    for n,freq in enumerate(frequencies):
        print('doing frequency: ', freq)
        #trap off
        set_lo = lo_pype.Set("lo_cw_freq", freq).Wait()
        trap_off = trap_pype.Set("trap_output", "OFF").Wait()
        mantis_kwargs.update({"output":file_prefix+str(n)+'_trap_off'})
        lo_pype.RunMantis(**mantis_kwargs)
        #trap on
        trap_on = trap_pype.Set("trap_output", "ON").Wait()
        mantis_kwargs.update({"output":file_prefix+str(n)+'_trap_on'})
        lo_pype.RunMantis(**mantis_kwargs)
        trap_off = trap_pype.Set("trap_output", "OFF").Wait()

if __name__ == "__main__":
    if len(sys.argv) == 2
        config = open(sys.argv[1])
        conf_dict = json.load(config)
        full_spectrum(conf_dict)
    else:
        print("usage: $ ./full_spectrum.py /path/to/config.json")
