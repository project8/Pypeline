#!/bin/bash

# Watch that the night_run is working

RUNDATE=20140613
SESSION=python_night_run

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
	sleep 10
	echo restarting Ignatius
	ssh root@ignatius 'shutdown -h now'
	sleep 120
	echo Wake up ignatius
	wol 00:25:90:15:2f:b3
	sleep 180
	echo Start DAQ
	ssh ignatius '~/Code/AntFarm/start_daq.sh'
	sleep 60
	echo Start Acquisition
	tmux attach-session -d -s ${SESSION}
	tmux select-pane -t ${SESSION}:1.0
	tmux send-keys "rate_vs_time_study ~/night_run.json" C-m
	echo Everything should be working now
	sleep 60
fi

