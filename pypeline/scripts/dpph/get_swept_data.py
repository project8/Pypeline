#!/usr/bin/python2

#from pypeline import DripInterface

from time import sleep


def SweepDPPHData(pype):
    sweep_time_s = 1
    sample_period_ms = 10
    sample_length = int(sweep_time_s * 1000 / sample_period_ms)
    print("sample length is", str(sample_length))
    #pype = DripInterface('http://myrna.phys.washington.edu:5984')
    pype.Set('lockin_raw_write', "NC").Wait()
    pype.Set('lockin_raw_write', "CBD 51").Wait()
    pype.Set('lockin_raw_write', "LEN " + str(sample_length)).Wait()
    pype.Set('lockin_raw_write', "STR " + str(int(sample_period_ms))).Wait()
    pype.Set('lockin_raw_write', "TD").Wait()
    sleep(2 * sample_length/1000)
    adc_curve=pype.Get('lockin_adc1_curve').Wait()['final']
    x_curve=pype.Get('lockin_x_curve').Wait()['final']
    y_curve=pype.Get('lockin_y_curve').Wait()['final']
    print("lengths: x "+str(len(x_curve))+" y "+str(len(y_curve))+" adc "+str(len(adc_curve)))
    for i in range(len(adc_curve)):
        print(str(x_curve[i])+" "+str(y_curve[i])+" "+str(adc_curve[i]))
