import asyncio
from bleak import BleakClient

address = "E0:C6:BC:1A:E7:A9"
MODEL_NBR_UUID = ""

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NUBR_UUID)
        print("Model number: {0}".format("".join( map(chr, model_number) ) ) )
