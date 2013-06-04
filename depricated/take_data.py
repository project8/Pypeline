#!/usr/bin/env python2.7
import time
import string
from pypeline import DripInterface

def dro_freq():
	return 24500

def lo_cw_tgt(freq):
	return freq - dro_freq() - 50

def trap_zero():
	return "2.705V"

def trapping():
	return "0.4V"

def anti_trapping():
	return "5.0V"

def make_runname(lo_freq,trap_status):
	return "/data/run_LO"+str(lo_freq)+"_"+time.strftime("%Y_%m_%d_%H:%M:%S")+"_"+trap_status+".egg"

def do_run(runname,drip):
	print "digitizing to file ",runname
	drip.Run(rate=200,duration=20000,filename=runname).Wait(timeout=100)
	time.sleep(1)

def run_at(frequency, drip):
	print("running at LO={0}".format(frequency))

	# use dripline interface to set frequency to frequency.  switch from
	# print to the drip.Set thing that is the argument to print
	print("drip.Set('lo_cw_freq',str(frequency))")
	drip.Set('lo_cw_freq',str(frequency))

	# set trap current to zero, sleep to let current settle, 
	# and run with some descriptive filename.  wait for Run to return
	# before proceeding.
	print("drip.Set('trap_current',str(trap_zero()))")
	drip.Set('trap_current',str(trap_zero()))
	time.sleep(10)
	for i in range(5):
		runname=make_runname(frequency,"trap_off")
		do_run(runname,drip)

	# set trap to trapping mode and run again
	print("drip.Set('trap_current',str(trapping()))")
	drip.Set('trap_current',str(trapping()))
	time.sleep(5)
	for i in range(5):
		runname=make_runname(frequency,"trap_on")
		do_run(runname,drip)
	#print("run.Wait()")

	# set trap to anti-trapping and run again
	print("drip.Set('trap_current',str(anti_trapping()))")
	drip.Set('trap_current',str(anti_trapping()))
	time.sleep(5)
	for i in range(5):
		runname=make_runname(frequency,"trap_anti")
		do_run(runname,drip)
	#print("run.Wait()")


def main():
	# first calculate the local oscillator frequencies we want to run at
	lo_frequencies = map(lambda x: lo_cw_tgt(x), range(25000, 27000, 40))

	# now get a dripline object.  commmented out b/c i don't have library,
	# replace 0 with a DripInterface
	#drip = 0 # DripInterface()
	#drip=DripInterface.DripInterface('http://p8portal.phys.washington.edu:5984')
	drip=DripInterface('http://p8portal.phys.washington.edu:5984')

	# now run.  maybe check that drip is a reasonable thing first?
	map(lambda f: run_at(f, drip), lo_frequencies)

if __name__ == '__main__':
	main()
