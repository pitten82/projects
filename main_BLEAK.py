"""
Notifications
-------------
Example showing how to add notifications to a characteristic and handle the responses.
Updated on 2019-07-03 by hbldh <henrik.blidh@gmail.com>
"""

import sys
import logging
import asyncio
import platform

from bleak import BleakClient
from bleak import _logger as logger
import bleak

ADDRESS = ("F8:8A:5E:36:CB:34")  # <--- Change to your device's address here if you are using Windows or Linux
CHARACTERISTIC_UUID_1 = "835ab4c0-51e4-11e3-a5bd-0002a5d5c51b"  # <--- Change to the characteristic you want to enable notifications from.
CHARACTERISTIC_UUID_2 = "00002a1c-0000-1000-8000-00805f9b34fb"  # <--- Change to the characteristic you want to enable notifications from.



if len(sys.argv) == 3:
    ADDRESS = sys.argv[1]
    CHARACTERISTIC_UUID_1 = sys.argv[2]


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def run(address, debug=True):
    if debug:
        import sys

        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address) as client:
        # logger.info(f"Connected: {client.is_connected}")
        print(f"Connected: {client.is_connected}")

        await client.start_notify(CHARACTERISTIC_UUID_1, notification_handler)
        await client.start_notify(CHARACTERISTIC_UUID_2, notification_handler)
        await asyncio.sleep(60.0)
        await client.stop_notify(CHARACTERISTIC_UUID_1)
        await client.stop_notify(CHARACTERISTIC_UUID_2)
        await client.disconnect()

if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(ADDRESS, True))