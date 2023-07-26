# import paho.mqtt.client as paho
# from paho import mqtt
import asyncio
import aiofiles
import aiomqtt
import threading
import logging
from queue import Queue
import struct
import time
import re
from utils.preprocessing import ForMeasurement
import pyarrow.vendored.version
import os
import sys
import numpy as np
from tensorflow.keras import models
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from PIL import Image
import io

"""
1. 다수의 파일
2. 파일에 누적되는 데이터 수집 완료 후 사용자가 직접 Software 버튼 눌러서 데이터 송신
"""

"""
update 2023-07-25
기존 사용 방식
- Observer에 MQTTtool 객체 인스턴스 생성 이후 Thread를 시작하고, Queue에 file_path를 추가하여 한 파일씩 보내던 방식

수정 방식
- Thread의 생성자에서 file_path를 입력으로 받음
- 한 Thread가 여러 파일을 담당하지 않고, 파일 생성 이벤트에 의해 감지된 각 파일 별 Thread를 생성하여 개별 파일마다 개별 쓰레드가 해당 파일 내용 전송을 담당하도록 함
"""


# class MQTTtool(threading.Thread):
#     def __init__(self, file_path: str, interval) -> None:
#         threading.Thread.__init__(self, daemon=True)
#         self.file_path = file_path
#         self.interval = interval
#         self.fm = ForMeasurement()

#     def on_connect(self, client, userdata, flags, rc, properties=None) -> None:
#         if rc == 0:
#             logging.info("Connected with MQTT broker. code : " + str(rc))
#         else:
#             logging.info("Failed connect with MQTT broker. code : " + str(rc))

#     def on_publish(self, client, userdata, mid, properties=None) -> None:
#         return
#         # logging.info(str(mid) + " sent to MQTT broker.")

#     def on_disconnect(self, client, userdata, flags, rc=0) -> None:
#         logging.info("Disconnected with MQTT broker. code : " + str(rc))

#     def connectBroker(
#         self, address: str, port: int, username: str, pw: str
#     ) -> paho.Client:
#         client = paho.Client(client_id="test_pub", userdata=None, protocol=paho.MQTTv5)
#         # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

#         client.on_connect = self.on_connect
#         client.on_publish = self.on_publish
#         client.on_disconnect = self.on_disconnect

#         client.username_pw_set(username, pw)
#         client.connect(address, port)

#         return client

#     def publishData(self, topic: str, msg: str) -> None:
#         self.client.publish(topic, msg, 0)

#     def disconnectBroker(self) -> None:
#         self.client.disconnect()

#     def run(self) -> None:
#         """
#         qos 1, 2로 publish 시 짧은 interval로 여러 msg 전송 불가
#         qos 0일 시 client가 on_connect callback 응답받기 전에 publish 실행됨
#         qos 0으로 publish하면서 해당 문제 해결을 위해 연결 이후 1초 sleep
#         """
#         # self.client = self.connectBroker(
#         #     "f6bab081112e4de99897d2ceee683056.s1.eu.hivemq.cloud",
#         #     8883,
#         #     "banfsensors",
#         #     "qksvmtpstj!#",
#         # )

#         self.client = self.connectBroker(
#             "server.banf.co.kr",
#             1883,
#             "banfsensors",
#             "qksvmtpstj!#",
#         )

#         cur_file_size = os.path.getsize(self.file_path)

#         time.sleep(1)  # for on_connect callback on qos 0

#         self.client.loop_start()

#         cnt = 0
#         while True:
#             # file_size = os.path.getsize(self.file_path)
#             # if cur_file_size - file_size == 0:
#             #     break
#             # logging.info(f"mqtt, {self.file_path} sending...")

#             # packet_chunk_list = self.fm.transformFileToSendPacket(self.file_path)

#             # for packet_chunk in packet_chunk_list:
#             #     self.publishData("banf/sensors", packet_chunk)
#             #     # time.sleep(0.01)
#             # logging.info(f"{self.file_path} send complete!")

#             # cur_file_size = file_size
#             self.publishData("banf/sensors", f"test : {cnt}")
#             cnt += 1
#             time.sleep(self.interval)

#         time.sleep(0.5)

#         self.client.loop_stop()
#         time.sleep(0.5)

#         self.disconnectBroker()


class MQTTtool(threading.Thread):
    def __init__(self, file_path: str, interval, model) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.CHUNK_SIZE = 500
        self.file_path = file_path
        self.interval = interval
        self.model = model
        self.last_read_line = 0
        self.fm = ForMeasurement()
        if sys.platform.lower() == "win32" or os.name.lower() == "nt":
            logging.info(
                "Windows OS detected. Set asyncio event loop policy to WindowsSelectorEventLoopPolicy"
            )
            from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

            set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    def extract_acc_z(self, lines: list):
        lines_2d = [line.split("\t") for line in lines]

        acc_x_raw = np.array(list(zip(*lines_2d))[1]).astype(np.float64)
        acc_y_raw = np.array(list(zip(*lines_2d))[2]).astype(np.float64)
        acc_z_raw = np.array(list(zip(*lines_2d))[3]).astype(np.float64)

        acc_x_raw[acc_x_raw > 32767] -= 65536
        acc_y_raw[acc_y_raw > 32767] -= 65536
        acc_z_raw[acc_z_raw > 32767] -= 65536

        acc_x = ((acc_x_raw * 0.0001007080078) + 1.65 - 1.65) * 800
        acc_y = ((acc_y_raw * 0.0001007080078) + 1.65 - 1.65) * 800
        acc_z = ((acc_z_raw * 0.0001007080078) + 1.65 - 1.65) * 800

        logging.info(f"acc_x[:10] : {acc_x[:10]}")
        logging.info(f"acc_y[:10] : {acc_y[:10]}")
        logging.info(f"acc_z[:10] : {acc_z[:10]}")
        return [acc_x, acc_y, acc_z]

    def single_axis_spectrogram_image(self, signal: np.ndarray):
        signal = [
            signal[i : i + self.CHUNK_SIZE]
            for i in range(0, len(signal), self.CHUNK_SIZE)
        ]
        fig, ax = plt.subplots(frameon=False)

        img_list = []

        for s in signal:
            f, t, Sxx = spectrogram(s, fs=1000, nperseg=32, noverlap=28)
            ax.set_axis_off()
            ax.set_aspect("auto")
            ax.pcolormesh(t, f, Sxx, cmap="bone")
            plt.show()

            img_buf = io.BytesIO()
            fig.savefig(img_buf, bbox_inches="tight", pad_inches=0, dpi=100)

            img = Image.open(img_buf)
            img = img.resize((500, 500))
            img_buf.close()
            img_list.append(img)

        return img_list

    async def publish_message_iteration(self, topic: str) -> None:
        cur_file_size = os.path.getsize(self.file_path)

        await asyncio.sleep(1)

        async with aiomqtt.client.Client("server.banf.co.kr", 1883) as client:
            while True:
                # logging.info(f"self.last_read_line = {self.last_read_line}")
                file_size = os.path.getsize(self.file_path)

                if cur_file_size - file_size == 0:
                    break
                async with aiofiles.open(self.file_path, "r") as f:
                    await f.seek(self.last_read_line)
                    all_lines = await f.readlines()

                    num_chunks = len(all_lines) // self.CHUNK_SIZE

                    lines = all_lines[: num_chunks * self.CHUNK_SIZE]

                    self.last_read_line += (
                        len("\n".join(lines)) + 1
                    )  # 실제 f.tell()에 의한 위치는 라인 별 개행 및 맨 마지막 개행을 포함한 것으로 보임

                    # self.last_read_line = await f.tell()

                logging.info(f"lines length : {len(lines)}")
                three_acc_list = self.extract_acc_z(lines)

                self.single_axis_spectrogram_image(three_acc_list[0])

                # lines.insert(0, self.file_path)

                # packet_chunk_list = self.fm.transformToSendPacket(lines)
                # for packet_chunk in packet_chunk_list:
                #     await client.publish(topic, packet_chunk, qos=0)

                # # logging.info(f"MQTT Message Sended. : {packet_chunk}")
                # logging.info(f"payload length : {len(lines[1:])}")
                await asyncio.sleep(self.interval)
                cur_file_size = file_size
            logging.info(f"Stop Thread - {self.file_path}")

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.publish_message_iteration("banf/sensors"))
