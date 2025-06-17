import argparse # easy bash-to-python info passing
import asyncio # asynchronous connections
import struct # allows data unpacking
from bleak import BleakClient

TMP_CHAR_UUID = "00002235-b38d-4985-720e-0f993a68ee41"
HUM_CHAR_UUID = "00001235-b38d-4985-720e-0f993a68ee41"

sleep_time = 5 # seconds between data pulls
max_time = 60 # maximum wait time before error

# --- DECODE SENSOR DATA STREAM --- #
def parse_sensor_data(traw, hraw):
    # Data is in bytearray format, '<f' = little-endian float
    t = struct.unpack('<f', traw)[0]
    h = struct.unpack('<f', hraw)[0]
    return t, h

async def stream_data(client):
    while True:
        try:
            tmp_raw = await client.read_gatt_char(TMP_CHAR_UUID)
            hum_raw = await client.read_gatt_char(HUM_CHAR_UUID)
            temperature, humidity = parse_sensor_data(tmp_raw, hum_raw)
            print(f"Reading {address}")
            print(f"Temperature: {temperature}")
            print(f"Humidity: {humidity}")
        except Exception as e:
            print(f"Failed for {address}: {e}")
        await asyncio.sleep(sleep_time)

async def main(address):
    async with BleakClient(address, timeout=max_time) as client:
        await read_loop(client)

# --- PARSE NAME, ADDRESS ARGUMENTS AND RUN --- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to SHT via MAC address"
    )
    parser.add_argument(
        '--address',
        type=str,
        required=True,
        help='MAC address of the BLE device (e.g., AA:BB:CC:DD:EE:FF)'
    )
    args        = parser.parse_args()
    address     = args.address

    asyncio.run(main(address))
