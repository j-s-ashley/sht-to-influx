import argparse # easy bash-to-python info passing
import asyncio # asynchronous connections
import struct # allows data unpacking
from bleak import BleakScanner
from bleak import BleakClient

def parse_sensor_data(data: bytes):
    temp_raw, hum_raw = struct.unpack("<HH", data)
    temperature = -45 + (175 * temp_raw / 65535.0)
    humidity = 100 * hum_raw / 65535.0
    return temperature, humidity

async def main(device_name, address):
    with BleakClient(address, timeout=60.0) as client:
        try:
            data = await client.read_gatt_char(CHAR_UUID)
                temperature, humidity = parse_sensor_data(data)
                print(f"Reading {a}")
                print(f"Temperature: {temperature}")
                print(f"Humidity: {humidity}")
                #print(f"data output: {data}")
        except Exception as e:
            print(f"Failed for {a}: {e}")

# --- PARSE NAME, ADDRESS ARGUMENTS AND RUN --- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to SHT via MAC address"
    )
    parser.add_argument(
        '--device_name',
        type=str,
        required=True,
        help='Custom name of the BLE device (e.g., sht-julio)'
    )
    parser.add_argument(
        '--address',
        type=str,
        required=True,
        help='MAC address of the BLE device (e.g., AA:BB:CC:DD:EE:FF)'
    )
    args        = parser.parse_args()
    device_name = args.device_name
    address     = args.address

    asyncio.run(main(device_name, address))
