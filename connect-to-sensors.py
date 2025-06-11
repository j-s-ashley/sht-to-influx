import asyncio
import json
from bleak import BleakClient

TEMPERATURE_CHAR_UUID = "00002235-b38d-4985-720e-0f993a68ee41"
HUMIDITY_CHAR_UUID    = "00001235-b38d-4985-720e-0f993a68ee41"

async def read_sensor(name, mac):
    async with BleakClient(mac) as client:
        print(f"\nConnected to {name} ({mac})")

        async def handle_temperature(_, data):
            temp_c = int.from_bytes(data, byteorder='little', signed=True) / 100
            print(f"[{name}] Temperature: {temp_c:.2f}")

        async def handle_humidity(_, data):
            humidity = int.from_bytes(data, byteorder='little') / 100
            print(f"[{name}] Humidity: {humidity:.2f}")

        await client.start_notify(TEMPERATURE_CHAR_UUID, handle_temperature)
        await client.start_notify(HUMIDITY_CHAR_UUID, handle_humidity)

        await asyncio.sleep(10)  # Stream for 10 seconds

        await client.stop_notify(TEMPERATURE_CHAR_UUID)
        await client.stop_notify(HUMIDITY_CHAR_UUID)
        print(f"Disconnected from {name}")

async def main():
    with open("docs/sensor-info.json", "r") as f:
        sensors = json.load(f)

    for sensor in sensors:
        try:
            await read_sensor(sensor["device_name"], sensor["address"])
        except Exception as e:
            print(f"Error with {sensor['device_name']} ({sensor['address']}): {e}")


if __name__ == "__main__":
    asyncio.run(main())
