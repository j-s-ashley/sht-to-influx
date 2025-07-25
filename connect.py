import argparse # easy bash-to-python info passing
import asyncio # asynchronous connections
import struct # allows data unpacking
import sys 
from bleak import BleakClient, BleakError

# --- DEFINITIONS --- #
# ID for battery level, bluetooth default
BTR_CHAR_UUID = "00002A19-0000-1000-8000-00805f9b34fb"
# These are vendor-specific IDs for the temperature/humidity data
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
            btr_raw = await client.read_gatt_char(BTR_CHAR_UUID)
            tmp_raw = await client.read_gatt_char(TMP_CHAR_UUID)
            hum_raw = await client.read_gatt_char(HUM_CHAR_UUID)
            battery = int(btr_raw[0])
            temperature, humidity = parse_sensor_data(tmp_raw, hum_raw)
            print(f"{battery}\t{temperature}\t{humidity}")
            sys.stdout.flush()
        except BleakError as e:
            print(f"BleakError: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)
        await asyncio.sleep(sleep_time)

async def main(address):
    async with BleakClient(address, timeout=max_time) as client:
        print("Battery\tTemperature\tHumidity")
        sys.stdout.flush()
        await stream_data(client)

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
