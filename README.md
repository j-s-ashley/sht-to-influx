Relatively painless SHT3x and SHT4x connection to inFlux database!

# Step 1 - Set up a Raspberry Pi

The machine should be located somewhere physically close (within ~2 meters) by the SHTs. In addition to a power supply, it will need internet access. So far, this set up has not been tested with WiFi. Good luck.

# Step 2 - Clone this git repo

**Important note**: You will need the submodule `moneater`, so be sure to include the `--recurse-submodules` flag. If you ignored this important note on the first go and have already cloned this repo, you can use `git submodule update --init --recursive` to initialize, fetch, and checkout `moneater`.

## HTTPS

https://github.com/j-s-ashley/sht-to-influx.git --recurse-submodules

## SSH
git@github.com:j-s-ashley/sht-to-influx.git --recurse-submodules

# Step 3 - Update your Sensor List

Change the info for each sensor in [sensor-list.json](https://github.com/j-s-ashley/sht-to-influx/blob/main/config/sensor-list.json) to reflect its MAC address and location. Other fields are optional but recommended for bookkeeping purposes.

The key you use for a sensor (e.g., `sht-sally`) will define the name of the background service used to manage your sensor. The `device_id` is the 14-digit code above the QR code on the back of the sensor (the only reliable unique physical identifier for these sensors).

To find the MAC address, turn on one sensor at a time and run `bluetoothctl devices`. Look for a device with the name "Smart Humigadget" (for SHT31s) or "SHT40 Gadget" for (SHT4xs).

The location of the sensor will display in whatever Grafana visualizer you set up. Descriptive is best.

# Set 4 - Update RPi Name Variables

The [setup](https://github.com/j-s-ashley/sht-to-influx/blob/main/setup), [run-pipeline](https://github.com/j-s-ashley/sht-to-influx/blob/main/run-pipeline), and [monitor-pipeline](https://github.com/j-s-ashley/sht-to-influx/blob/main/monitor-pipeline) executables all contain the variable `PI_NAME`, which must be changed to the name of the Raspberry Pi on which you are setting this up.

Additionally, you must change the default name, `dewypi`, to the name of your Raspberry Pi in [sht@.service](https://github.com/j-s-ashley/sht-to-influx/blob/main/sht%40.service) and [monitor-sht@.service](https://github.com/j-s-ashley/sht-to-influx/blob/main/monitor-sht%40.service).

# Step 5 - Run `setup`

**This must be done as super user.**

In the repo, run

`sudo ./setup`

This script:
 - ensures your Pi has the necessary software packages
 - creates a Python virtual environment with all necessary Python packages
 - sets up individual services for each sensor in [sensor-list.json](https://github.com/j-s-ashley/sht-to-influx/blob/main/config/sensor-list.json)
