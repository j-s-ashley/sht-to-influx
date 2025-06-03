import asyncio
from bleak import BleakScanner

async def main():
    async with BleakScanner() as scanner:
        print("Scanning...")

        n = 15
        print(f"\n{n} advertisement packets:")
        async for bd, ad in scanner.advertisement_data():
            if 'Smart Humigadget' in ad:
                print(f" {n}. {bd!r} with {ad!r}")
            n -= 1
            if n == 0:
                break

if __name__ == "__main__":
    asyncio.run(main())
