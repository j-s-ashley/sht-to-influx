import argparse
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import struct

# --- DEFINITIONS --- #
# Allow CLI tags for stuff like OS-specific operation
class Args(argparse.Namespace):
    macos_use_bdaddr: bool
    services: list[str]

device_name = 'Smart Humigadget'
addresses = []

# Look for bluetooth devices and grab address info
async def main(args: Args):
    print("scanning for 10 seconds, please wait...")

    devices = await BleakScanner.discover(
        return_adv=True,
        service_uuids=args.services,
        cb={"use_bdaddr": args.macos_use_bdaddr},
        timeout=10.0,
    )

    print("Getting MAC addresses...")
    for d, a in devices.values():
        if device_name in a:
            suffix = ': ' + device_name 
            address = str(d).replace(suffix, "")
            addresses.append(address)

# What to do if CLI tag is provided for a specific UUID or MacOS
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--services",
            metavar="<uuid>",
            nargs="*",
            help="UUIDs of one or more services to filter for",
        )
    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )
    args = parser.parse_args(namespace=Args())
    asyncio.run(main(args)) 

# Connect to each address
for a in addresses:
    print(f"Connecting to {a}")
    async def main(a):
        async with BleakClient(a, timeout=15.0) as client:
            services = await client.get_services()
    asyncio.run(main(a))

CHAR_UUID = "2235"
"""
    This UUID was hard to find.
    It was found in line 39 of LoggerService.cpp in the SHT31 Firmware
    GitHub repository, linked here:
    https://github.com/Sensirion/SmartGadget-Firmware/blob/0fca4bb74585b576a5d25e05ef89a22b69b701a8/BLE_Module_nRF51822/source/services/LoggerService.cpp#L39
    Custom UUIDs for the humidity and temperature data streams seem to be
    stored in the containing directory as well, but do not *currently*
    appear to be necessary.
"""

def parse_sensor_data(data: bytes):
    temp_raw, hum_raw = struct.unpack("<HH", data)
    temperature = -45 + (175 * temp_raw / 65535.0)
    humidity = 100 * hum_raw / 65535.0
    return temperature, humidity

async def read_sensor_data():
    for a in addresses:
        try:
            async with BleakClient(a) as client:
                data = await client.read_gatt_char(CHAR_UUID)
                #temperature, humidity = parse_sensor_data(data)
                
                print(f"Reading {a}")
                #print(f"Temperature: {temperature}")
                #print(f"Humidity: {humidity}")
                print(f"data output: {data}")

        except Exception as e:
            print(f"Failed for {a}: {e}")

asyncio.run(read_sensor_data())
