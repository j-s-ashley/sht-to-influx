import argparse
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import struct

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

async def main(a):
    print(f"Connecting to {a}")
    async with BleakClient(a, timeout=90.0) as client:
        services = await client.get_services()

asyncio.run(main(address))

LOG_SRVC_UUID: "0000f234-b38d-4985-720e-0f993a68ee41"
LOG_CHAR_UUID: "0000f238-b38d-4985-720e-0f993a68ee41"
TMP_CHAR_UUID: "00002235-b38d-4985-720e-0f993a68ee41"
HUM_CHAR_UUID: "00001235-b38d-4985-720e-0f993a68ee41"

#def parse_sensor_data(data: bytes):
#    temp_raw, hum_raw = struct.unpack("<HH", data)
#    temperature = -45 + (175 * temp_raw / 65535.0)
#    humidity = 100 * hum_raw / 65535.0
#    return temperature, humidity

async def read_sensor_data():
    try:
        async with BleakClient(address, timeout=90.0) as client:
            #data = await client.read_gatt_char(CHAR_UUID)
            #temperature, humidity = parse_sensor_data(data)
                
            print(f"Reading data stream from {address}")
            temperature = await client.read_gatt_char(TMP_CHAR_UUID)
            humidity    = await client.read_gatt_char(HUM_CHAR_UUID)
            #print(f"Temperature: {temperature}")
            #print(f"Humidity: {humidity}")
            print("Temperature\tRelative Humidity")
            print(f"{temperature}\t{humidity}")

    except Exception as e:
        print(f"Failed for {address}: {e}")

asyncio.run(read_sensor_data())
