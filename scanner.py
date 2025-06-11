import argparse
import asyncio
from bleak import BleakClient

async def main(a):
    async with BleakClient(a, timeout=30.0) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid} | {service.description}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} | {char.description}")

if __name__ == "__main__":
    # parse name, address arguments
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
    
    # do the things
    asyncio.run(main(address))
