#!/bin/bash

USR=$1
PWRD=$2

ADDRESS=$3
LOCATION=$4

source ${HOME}/sht-to-influx/sht-venv/bin/activate

python ${HOME}/sht-to-influx/connect.py --address $ADDRESS | tee /dev/tty | python ${HOME}/moneater/moneater.py eaters.tabeater.TabEater --host 128.3.50.38 --port 8086 --database strips_environmental --user $USR --password $PWRD --table TempHum --tag Name=$LOCATION
PID=$!

MAX_WAIT=60
SUCCESSFUL=false
ATTEMPT=0

while true; do
    for (( i=0; i<$MAX_WAIT; i++ )); do
        if bluetoothctl info $ADDRESS | grep -q 'Connected: yes'; then
            SUCCESSFUL=true
        else
            SUCCESSFUL=false
        fi
        sleep 1
    done
    
    if [[ "$SUCCESSFUL" = false ]]; then
        ((ATTEMPT++))
        echo "Sensor at $LOCATION timed out, killing connection attempt $ATTEMPT with process $PID"
        kill -9 $PID
        python ${HOME}/sht-to-influx/connect.py --address $ADDRESS | tee /dev/tty | python ${HOME}/moneater/moneater.py eaters.tabeater.TabEater --host 128.3.50.38 --port 8086 --database strips_environmental --user $USR --password $PWRD --table TempHum --tag Name=$LOCATION
        PID=$!
    fi
done
