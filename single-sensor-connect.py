import struct # used for parsing raw data streams
import asyncio # prevents BLE bottlenecking
import argparse # allows CLI argument passing
from bleak import BleakClient # allows BLE connection

TMP_CHAR_UUID = "00002235-b38d-4985-720e-0f993a68ee41"
HUM_CHAR_UUID = "00001235-b38d-4985-720e-0f993a68ee41"

# --- DECODE SENSOR DATA STREAM --- #
def parse_sensor_data(traw, hraw):
    # Data is in bytearray format, '<f' = little-endian float
    t = struct.unpack('<f', traw)[0]
    h = struct.unpack('<f', hraw)[0]
    return t, h

# --- CONNECT TO SENSOR & READ DATA STREAM --- #
async def main(name, address):
    #print("Device Name\tTemperature\tRelative Humidity")

    while True:
        try:
            async with BleakClient(address, timeout=90.0) as client:
                tmp_raw = await client.read_gatt_char(TMP_CHAR_UUID)
                hum_raw = await client.read_gatt_char(HUM_CHAR_UUID)
                temperature, humidity = parse_sensor_data(tmp_raw, hum_raw)
                print(f"{name}\t{temperature}\t{humidity}")

        except Exception as e:
            print(f"Failed for {address}: {e}")
        await asyncio.sleep(1)

# --- OUTPUT DATA --- #
if __name__ == "__main__":
    # parse address argument
    parser = argparse.ArgumentParser(
        description="Connect to SHT via MAC address"
    )
    parser.add_argument(
        '--name', 
        type=str, 
        required=True, 
        help='Custom name of the BLE device'
    )
    parser.add_argument(
        '--address', 
        type=str, 
        required=True, 
        help='MAC address of the BLE device (e.g., AA:BB:CC:DD:EE:FF)'
    )
    args    = parser.parse_args()
    address = args.address
    
    # do the things
    asyncio.run(main(name, address))
