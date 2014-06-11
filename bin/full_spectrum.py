#!/usr/bin/python

from __future__ import print_function

import pypeline
import subprocess

frequencies = range(400, 1401, 10)
lo_pype = pypeline.DripInterface("http://myrna.phys.washington.edu:5984")
trap_pype = pypeline.DripInterface("http://higgsino.physics.ucsb.edu:5984")

def Digitize(filename, lo):
    temp_conf = open("full_spectrum_mantis_temp.json", "w")
    subprocess.call(['sed', 's/FILENAME/{:s}/'.format(filename), 'full_spectrum_mantis_template.json'], stdout=temp_conf)
    temp_conf.close()
    subprocess.call(['sed', '-i', 's/LOFREQ/%i/'%lo, 'full_spectrum_mantis_temp.json'])
    subprocess.call(['cat full_spectrum_mantis_temp.json | ssh ignatius "cat > temp.json"'], shell=True)
    subprocess.call(['ssh','ignatius','/usr/local/bin/mantis_client','config=~/temp.json'])

for n,freq in enumerate(frequencies):
    print('doing frequency: ', freq)
    set_lo = lo_pype.Set("lo_cw_freq", freq).Wait()
    trap_off = trap_pype.Set("trap_output", "OFF").Wait()
    Digitize('run_%iMHz_off.egg'%freq, freq)
    trap_on = trap_pype.Set("trap_output", "ON").Wait()
    Digitize('run_%iMHz_on.egg'%freq, freq)
    trap_off = trap_pype.Set("trap_output", "OFF").Wait()
