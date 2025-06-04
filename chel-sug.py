import asyncio
from bleak import BleakClient
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import struct

# Replace these:
SENSOR_ADDRESSES = ["XX:XX:XX:XX:XX:01", "XX:XX:XX:XX:XX:02"]  # Add all 7
CHAR_UUID = "your-discovered-characteristic-uuid"
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "your-token"
INFLUX_ORG = "your-org"
INFLUX_BUCKET = "your-bucket"

def parse_sensor_data(data: bytes):
    # You will need to reverse-engineer or find the SHT31's GATT format
    # Example for two 16-bit little-endian ints (temperature and humidity):
    temp_raw, hum_raw = struct.unpack("<HH", data)
    temperature = -45 + (175 * temp_raw / 65535.0)
    humidity = 100 * hum_raw / 65535.0
    return temperature, humidity

async def read_and_send():
    influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = influx.write_api(write_options=SYNCHRONOUS)

    for addr in SENSOR_ADDRESSES:
        try:
            async with BleakClient(addr) as client:
                data = await client.read_gatt_char(CHAR_UUID)
                temperature, humidity = parse_sensor_data(data)

                point = Point("sht31")
                point.tag("device", addr)
                point.field("temperature", temperature)
                point.field("humidity", humidity)
                write_api.write(bucket=INFLUX_BUCKET, record=point)
        except Exception as e:
            print(f"Failed for {addr}: {e}")

asyncio.run(read_and_send())
