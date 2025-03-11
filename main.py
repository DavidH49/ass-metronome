import asyncio
import logging
import sys
import time
from buttplug import Client, Device, WebsocketConnector, ProtocolSpec


BPM = 153
T_VIB = 0.1
DELAY = 60 / BPM - T_VIB

WS_IP = "127.0.0.1"
WS_PORT = "12345"


async def main():
    client = Client("Ass Metronome", ProtocolSpec.v3)
    connector = WebsocketConnector(f"ws://{WS_IP}:{WS_PORT}", logger=client.logger)

    try:
        await client.connect(connector)
    except Exception as e:
        logging.error(f"Could not connect to server, exiting: {e}")
    
    client.logger.info(f"Devices: {client.devices}")

    if len(client.devices) != 0:
        device: Device = client.devices[0]

        if len(device.actuators) > 0:

            while True:
                t_start = time.process_time()

                await device.actuators[0].command(1)
                await asyncio.sleep(T_VIB)
                await device.actuators[0].command(0)
                
                delta = time.process_time() - t_start

                await asyncio.sleep(DELAY - delta)

    await client.disconnect()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    asyncio.run(main(), debug=True)