import argparse
import struct
import sys
import time
from bluepy.btle import Peripheral, DefaultDelegate, BTLEException

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

# --- PRIMARY DATA COLLECTION LOOP --- #
def stream_data(client):
    while True:
        try:
            btr_raw = peripheral.readCharacteristic(peripheral.getCharacteristics(uuid=BTR_CHAR_UUID)[0].getHandle())
            tmp_raw = peripheral.readCharacteristic(peripheral.getCharacteristics(uuid=TMP_CHAR_UUID)[0].getHandle())
            hum_raw = peripheral.readCharacteristic(peripheral.getCharacteristics(uuid=HUM_CHAR_UUID)[0].getHandle())

            battery = int(btr_raw[0])
            temperature, humidity = parse_sensor_data(tmp_raw, hum_raw)

            print(f"{battery}\t{temperature}\t{humidity}")

        except BTLEException as e:
            print(f"BTLEException: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

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

    try:
        peripheral = Peripheral(address)
        stream_data(peripheral)
    except BTLEException as e:
        print(f"Connection error: {e}", file=sys.stderr)
        sys.exit(2)
