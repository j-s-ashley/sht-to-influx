#!/bin/bash

USR=$1
PWRD=$2
ADDRESS=$3
LOCATION=$4

source ${HOME}/sht-to-influx/sht-venv/bin/activate

TIMER=0
MAX_WAIT=60
PID=0

run_sensor() {
    local usr="$1"
    local pwrd="$2"
    local address="$3"
    local location="$4"

    python ${HOME}/sht-to-influx/connect.py --address $address | tee /dev/tty | python ${HOME}/moneater/moneater.py eaters.tabeater.TabEater --host 128.3.50.38 --port 8086 --database strips_environmental --user $usr --password $pwrd --table TempHum --tag Name=$location
    PID=$!
}

monitor_connection() {
    while kill -0 "$PID" 2>/dev/null; do
        if ! bluetoothctl info $ADDRESS | grep -q 'Connected: yes'; then
            SUCCESSFUL=false
            if [ "$TIMER" -lt "$MAX_WAIT"]; then
                TIMER=$((TIMER + 15))
                sleep 15
            else
                echo "Sensor at $LOCATION timed out, killing connection attempt $ATTEMPT with process $PID"
                kill -9 $PID
                run_sensor "$USR" "$PWRD" "$ADDRESS" "$LOCATION" &
                PID=$!
            fi
        else
            SUCCESSFUL=true
        fi
        sleep 15
    done
}

run_sensor "$USR" "$PWRD" "$ADDRESS" "$LOCATION" &
monitor_connection
