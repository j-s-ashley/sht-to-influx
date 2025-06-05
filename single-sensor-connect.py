import struct # used for parsing raw data streams
import asyncio # prevents BLE bottlenecking
import argparse # allows CLI argument passing
from bleak import BleakClient # allows BLE connection

# --- PARSE ADDRESS ARGUMENT --- #
parser = argparse.ArgumentParser(
    description="Connect to SHT via MAC address"
)
parser.add_argument(
    '--address', 
    type=str, 
    required=True, 
    help='MAC address of the BLE device (e.g., AA:BB:CC:DD:EE:FF)'
)
args    = parser.parse_args()
address = args.address

# --- CONNECT TO SENSOR --- #
async def main(a):
    print(f"Connecting to {a}")
    async with BleakClient(a, timeout=90.0) as client:
        services = await client.get_services()

asyncio.run(main(address))

LOG_SRVC_UUID = "0000f234-b38d-4985-720e-0f993a68ee41"
LOG_CHAR_UUID = "0000f238-b38d-4985-720e-0f993a68ee41"
TMP_CHAR_UUID = "00002235-b38d-4985-720e-0f993a68ee41"
HUM_CHAR_UUID = "00001235-b38d-4985-720e-0f993a68ee41"

# --- DECODE DATA STREAM --- #
tmp_raw = bytearray(b'R\xb8\xb0A')
hum_raw = bytearray(b'\x9a\x99;B')


# --- READ DATA STREAM --- #
async def read_sensor_data():
    try:
        async with BleakClient(address, timeout=90.0) as client:
            print(f"Reading data stream from {address}")
            
            tmp_raw = await client.read_gatt_char(TMP_CHAR_UUID)
            hum_raw = await client.read_gatt_char(HUM_CHAR_UUID)
            
            # Data is in bytearray format, '<f' = little-endian float
            temperature = struct.unpack('<f', tmp_raw)[0]
            humidity    = struct.unpack('<f', hum_raw)[0]
            print("Temperature\tRelative Humidity")
            print(f"{temperature}\t{humidity}")

    except Exception as e:
        print(f"Failed for {address}: {e}")

asyncio.run(read_sensor_data())
