#!/bin/bash

# Watch that the night_run is working

RUNDATE=20140613

if [[ -n $(find /data/runs/$RUNDATE -mmin -10) ]]; then
	ls /data/runs/$RUNDATE
	echo
	echo All is fine
	echo waiting 5 minutes before checking again
	sleep 60
	echo waiting 4 minutes before checking again
	sleep 60
	echo waiting 3 minutes before checking again
	sleep 60
	echo waiting 2 minutes before checking again
	sleep 60
	echo waiting 1 minutes before checking again
	sleep 60
else
	echo Data acquisition stopped more than 10 minutes ago
	echo restarting Ignatius
	ssh root@ignatius 'shutdown -h now'
	sleep 120
	wol 00:25:90:15:2f:b3
	sleep 180
	ssh ignatius '~/Code/AntFarm/start_daq.sh'
	sleep 60

fi

