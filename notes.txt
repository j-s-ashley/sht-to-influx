# Day 1

okaly dokaly

running discover.py yields this tasty tidbit:

```
E0:C6:BC:1A:E7:A9: Smart Humigadget
-----------------------------------
AdvertisementData(local_name='Smart Humigadget', rssi=-64)
```

So, maybe all the ones we want to use will have that same `local_name` variable?? Would be super cool.

Okie dokie. Cap'n Crunch levels of fo-cereal now.

In trying to see about that `local_name` variable idea, I ended up discovering that the **ONE** button on these little doohickies does not function properly for most sensors.

What it's supposed to do:
 - Quick press: cycle between showing the dew point or relative humidity on the top line
 - Long press (>1s): enable/disable bluetooth connectivity
 - Hold down while inserting battery: switch between Celsius and Fahreneheit

What it actually does:
 - Quick press: sometimes freeze whatever numbers are displayed, sometimes display a blank screen for a few seconds, sometimes do nothing
 - Long press (>1s): same as quick press results
 - Hold down while inserting battery: switch between Celsius and Fahreneheit

I did, however, confirm that the `local_name` variable is consistent.

# Day 2

Apparently I have 2 days to do this :thumbs_up:

Alright. Let's find which UUIDs I need.

https://github.com/Sensirion/SmartGadget-Firmware/blob/master/BLE_Module_nRF51822/BLE_API/public/GattCharacteristic.h

This lists all the characteristic UUIDs, I think. Chel seems to agree.

Turns out that's the basic list. I think the UUIDs I need are defined here: 

 - Humidity - https://github.com/Sensirion/SmartGadget-Firmware/blob/master/BLE_Module_nRF51822/source/services/HumidityService.cpp
 - Temperature - https://github.com/Sensirion/SmartGadget-Firmware/blob/master/BLE_Module_nRF51822/source/services/TemperatureService.cpp

## Breaking it down

[Lines 32-33](https://github.com/Sensirion/SmartGadget-Firmware/blob/0fca4bb74585b576a5d25e05ef89a22b69b701a8/BLE_Module_nRF51822/source/services/HumidityService.cpp#L32-L33) of the `HumidityService.cpp` file:

```
const uint16_t HumidityServiceShortUUID = 0x1234;
const uint16_t HumidityServiceHumidityValueCharacteristicShortUUID = 0x1235;
```
 
[Lines 32-33](https://github.com/Sensirion/SmartGadget-Firmware/blob/0fca4bb74585b576a5d25e05ef89a22b69b701a8/BLE_Module_nRF51822/source/services/TemperatureService.cpp#L32-L33) of the `TemperatureService.cpp` file:
```
const uint16_t TemperatureServiceShortUUID = 0x2234;
const uint16_t TemperatureServiceTemperatureValueCharacteristicShortUUID = 0x2235;
```

These snippets imply that I ought to be able to use
 - `TEMPERATURE_UUID = 2235`
 - `HUMIDITY_UUID = 1235`
since we need the characteristic UUIDs. Right?


