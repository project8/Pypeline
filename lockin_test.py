#!/usr/bin/python2

from pypeline import DripInterface

from time import sleep

sweep_time_s=20
sample_period_ms=50
sample_length=int(sweep_time_s*1000/sample_period_ms)
print("sample length is"+str(sample_length))
drip=DripInterface('http://myrna.phys.washington.edu:5984')
drip.Set('lockin_raw_write',"NC").Wait()
drip.Set('lockin_raw_write',"CBD 51").Wait()
drip.Set('lockin_raw_write',"LEN "+str(sample_length)).Wait()
drip.Set('lockin_raw_write',"STR "+str(int(sample_period_ms))).Wait()
drip.Set('lockin_raw_write',"TD").Wait()
maxsleep=100
for i in range(maxsleep):
    sleep(1)
    statusfull=drip.Get('lockin_data_status').Wait()['final']
    status=statusfull[0]
    print(statusfull)
    if status=="0":
        break
adc_curve=drip.Get('lockin_adc1_curve').Wait()['final']
x_curve=drip.Get('lockin_x_curve').Wait()['final']
y_curve=drip.Get('lockin_y_curve').Wait()['final']
print("lengths: x "+str(len(x_curve))+" y "+str(len(y_curve))+" adc "+str(len(adc_curve)))
#for i in range(len(adc_curve)):
#    print(str(x_curve[i])+" "+str(y_curve[i])+" "+str(adc_curve[i]))
