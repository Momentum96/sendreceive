# import paho.mqtt.client as paho
# from paho import mqtt
import asyncio
import aiomqtt
import struct
import threading
import sys
import os

# from utils.send_receive import db_inserter
import logging


# class MQTTtool:
#     def __init__(self) -> None:
#         self.client = paho.Client(
#             client_id="test_sub", userdata=None, protocol=paho.MQTTv5
#         )
#         # self.db_tool = db_inserter.DBtool()
#         self.struct_fmt = "<2HB14HI2fi2dbdb2f"

#         # self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

#         self.client.on_connect = self.on_connect
#         self.client.on_disconnect = self.on_disconnect
#         self.client.on_subscribe = self.on_subscribe
#         self.client.on_message = self.on_message

#         self.client.username_pw_set("banfsensors", "qksvmtpstj!#")
#         self.client.connect("server.banf.co.kr", 1883)

#     def startSubscribe(self) -> None:
#         # self.db_tool.startThread()

#         self.client.subscribe("banf/sensors", qos=0)
#         self.client.loop_forever()

#     def on_connect(self, client, userdata, flags, rc, properties=None):
#         if rc == 0:
#             logging.info("connected OK")
#         else:
#             logging.info("Bad connection Returned code=", rc)

#     def on_disconnect(self, client, userdata, flags, rc=0):
#         logging.info("disconnected with MQTT broker. code :", str(rc))
#         # self.db_tool.stopThread()

#     def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
#         logging.info("subscribed: " + str(mid) + " " + str(granted_qos))

#     def on_message(self, client, userdata, msg):
#         # payload_list = [
#         #     list(i) for i in struct.iter_unpack(self.struct_fmt, msg.payload)
#         # ]
#         # print(payload_list)
#         logging.info(msg.payload)


class MQTTtool:
    def __init__(self) -> None:
        self.struct_fmt = "<2HB14HI2fi2dbdb2f"
        logging.info("MQTT Receiver is ready.")

        # self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    async def subscribe_message(self, topic: str) -> None:
        async with aiomqtt.client.Client(
            "server.banf.co.kr", 1883, client_id="test_sub"
        ) as client:
            await client.connect()
            await client.subscribe(topic, qos=0)

            while True:
                async with client.messages() as messages:
                    async for message in messages:
                        try:
                            payload_list = [
                                list(i)
                                for i in struct.iter_unpack(
                                    self.struct_fmt, message.payload
                                )
                            ]
                        except:
                            payload_list = [
                                list(i)
                                for i in struct.iter_unpack(
                                    self.struct_fmt[:10], message.payload
                                )
                            ]
                        # logging.info(f"MQTT Message Received. : {payload_list}")
                        logging.info(f"payload length : {len(payload_list)}")
                        # logging.info(f"{message.payload} - {message.topic}")
