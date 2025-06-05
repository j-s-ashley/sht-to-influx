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

## Timeout error

I keep getting this nonsense.

```
Traceback (most recent call last):
  File "/usr/lib64/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib64/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/opt/local/strips/ITk/sht31-to-influx/sensor-connect.py", line 57, in <module>
    asyncio.run(main(a))
  File "/usr/lib64/python3.9/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/usr/lib64/python3.9/asyncio/base_events.py", line 647, in run_until_complete
    return future.result()
  File "/opt/local/strips/ITk/sht31-to-influx/sensor-connect.py", line 55, in main
    async with BleakClient(a) as client:
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/__init__.py", line 570, in __aenter__
    await self.connect()
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/__init__.py", line 615, in connect
    return await self._backend.connect(**kwargs)
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/backends/bluezdbus/client.py", line 315, in connect
    raise
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/async_timeout/__init__.py", line 141, in __aexit__
    self._do_exit(exc_type)
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/async_timeout/__init__.py", line 228, in _do_exit
    raise asyncio.TimeoutError
asyncio.exceptions.TimeoutError
```
TODO: add link to GHI.

## Device disconnected error

```
Traceback (most recent call last):
  File "/usr/lib64/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib64/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/opt/local/strips/ITk/sht31-to-influx/sensor-connect.py", line 57, in <module>
    asyncio.run(main(a))
  File "/usr/lib64/python3.9/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/usr/lib64/python3.9/asyncio/base_events.py", line 647, in run_until_complete
    return future.result()
  File "/opt/local/strips/ITk/sht31-to-influx/sensor-connect.py", line 55, in main
    async with BleakClient(a, timeout=15.0) as client:
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/__init__.py", line 570, in __aenter__
    await self.connect()
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/__init__.py", line 615, in connect
    return await self._backend.connect(**kwargs)
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/backends/bluezdbus/client.py", line 273, in connect
    await self.get_services(
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/backends/bluezdbus/client.py", line 661, in get_services
    self.services = await manager.get_services(
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/backends/bluezdbus/manager.py", line 658, in get_services
    await self._wait_for_services_discovery(device_path)
  File "/opt/local/strips/ITk/sht31-to-influx/sht-venv/lib64/python3.9/site-packages/bleak/backends/bluezdbus/manager.py", line 791, in _wait_for_services_discovery
    raise BleakError("failed to discover services, device disconnected")
bleak.exc.BleakError: failed to discover services, device disconnected

```
# Day 3

Aight. Got some progress.

For the record:
"char_uuids": [
          "temperature": "00002235-b38d-4985-720e-0f993a68ee41",
          "humidity:     "00001235-b38d-4985-720e-0f993a68ee41"
      ]
