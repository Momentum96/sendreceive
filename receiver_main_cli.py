from utils.send_receive import mqtt_receiver
import asyncio
import sys
import os

# from utils.send_receive import kafka_consumer
import logging

logging.basicConfig(
    filename="./receiver-lte.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )

if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    logging.info(
        "Windows OS detected. Set asyncio event loop policy to WindowsSelectorEventLoopPolicy"
    )
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# mqtt_receiver.MQTTtool().startSubscribe()
# kafka_consumer.KAFKAtool().startSubscribe()


async def main():
    tool = mqtt_receiver.MQTTtool()
    await tool.subscribe_message("banf/sensors")


asyncio.run(main())
