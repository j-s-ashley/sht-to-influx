import argparse
import asyncio
from bleak import BleakScanner
from bleak import BleakClient

class Args(argparse.Namespace):
    macos_use_bdaddr: bool
    services: list[str]

device_name = 'Smart Humigadget'
addresses = []

async def main(args: Args):
    print("scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(
        return_adv=True,
        service_uuids=args.services,
        cb={"use_bdaddr": args.macos_use_bdaddr},
        timeout=10.0,
    )

    for d, a in devices.values():
        if device_name in a:
            suffix = ': ' + device_name 
            address = str(d).replace(suffix, "")
            addresses.append(address)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--services",
            metavar="<uuid>",
            nargs="*",
            help="UUIDs of one or more services to filter for",
        )
    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )
    args = parser.parse_args(namespace=Args())
    asyncio.run(main(args)) 

for a in addresses:
    print(a)
#    MODEL_NBR_UUID = "180A"
    async def main(a):
        async with BleakClient(a) as client:
            services = await client.get_services()
            for service in services:
                print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f" Characteristic: {char.uuid}, Properties: {char.properties}")
#            model_number = await client.read_gatt_char(MODEL_NUBR_UUID)
#            print("Model number: {0}".format("".join( map(chr, model_number) ) ) )

    asyncio.run(main(a))
