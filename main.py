import asyncio
import logging
import sys
import time
from buttplug import Client, Device, WebsocketConnector, ProtocolSpec


BPM = 130
T_VIB = 0.1


async def main():
    client = Client("Ass Metronome", ProtocolSpec.v3)
    connector = WebsocketConnector("ws://127.0.0.1:12345", logger=client.logger)

    try:
        await client.connect(connector)
    except Exception as e:
        logging.error(f"Could not connect to server, exiting: {e}")
    
    client.logger.info(f"Devices: {client.devices}")

    if len(client.devices) != 0:
        device: Device = client.devices[0]

        DELAY = 60 / BPM - T_VIB
        delta = 0

        while True:
            t_start = time.process_time()

            await device.actuators[0].command(1)
            await asyncio.sleep(T_VIB)
            await device.actuators[0].command(0)
            await asyncio.sleep(DELAY - delta)

            delta = time.process_time() - t_start

    await client.disconnect()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    asyncio.run(main(), debug=True)