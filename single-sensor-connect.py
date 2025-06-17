import struct # used for parsing raw data streams
import asyncio # prevents BLE bottlenecking
import argparse # allows CLI argument passing
from bleak import BleakClient # allows BLE connection

TMP_CHAR_UUID = "00002234-b38d-4985-720e-0f993a68ee41"
HUM_CHAR_UUID = "00001234-b38d-4985-720e-0f993a68ee41"

# --- DECODE SENSOR DATA STREAM --- #
def parse_sensor_data(traw, hraw):
    # Data is in bytearray format, '<f' = little-endian float
    t = struct.unpack('<f', traw)[0]
    h = struct.unpack('<f', hraw)[0]
    return t, h

# --- CONNECT TO SENSOR & READ DATA STREAM --- #
async def sensor_session(device_name, address, on_disconnect=None):
    client = BleakClient(address, disconnected_callback=lambda client: disconnect_event.set())
    disconnect_event = asyncio.Event()

    try:
        await client.connect()
        if not client.is_connected:
            raise RuntimeError("Connect failed")

        while client.is_connected:
            tmp_raw = await client.read_gatt_char(TMP_CHAR_UUID)
            hum_raw = await client.read_gatt_char(HUM_CHAR_UUID)
            temperature, humidity = parse_sensor_data(tmp_raw, hum_raw)

            print(f"{device_name}\t{temperature}\t{humidity}")
            await asyncio.sleep(poll_interval)

            if on_disconnect and disconnect_event.is_set():
                break
    finally:
        await client.disconnect()
        if on_disconnect:
            await on_disconnect()

async def main(device_name, address):
    while True:
        try:
            await sensor_session(
                device_name,
                address,
                on_disconnect=lambda: print("Disconnected – will reconnect in 5s") )
        except Exception as e:
            print(f"Session error: {e}")
        await asyncio.sleep(5)

# --- PARSE NAME, ADDRESS ARGUMENTS AND RUN --- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to SHT via MAC address"
    )
    parser.add_argument(
        '--device_name', 
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
    args        = parser.parse_args()
    device_name = args.device_name
    address     = args.address
    
    asyncio.run(main(device_name, address))
