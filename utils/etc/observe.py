from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import logging
from utils.etc import pattern
from utils.send_receive import mqtt_sender, s3_sender, prometheus_sender
from queue import Queue
from tensorflow.keras import models
import time
import os


# 파일 생성 이벤트 발생 시 실행할 내용
class MyEventHandler(FileSystemEventHandler):
    def __init__(
        self,
    ) -> None:
        self.model = models.load_model("./model_epoch_57.h5")
        logging.info("File Observer is ready.")

    def on_created(self, event) -> None:
        # TODO: process when a file created in the selected directory
        if event.event_type == "created" and event.is_directory == False:
            logging.info("{0} Created.".format(event.src_path.split("\\")[-1]))
            file_abs_path = event.src_path

            mqtt_sender.MQTTtool(file_abs_path, 1, self.model).start()


# 파일 생성 감지
class FileObserver(pattern.Singleton):
    def __init__(self) -> None:
        self.observer = None

    def setObserver(self, path: str) -> None:
        self.observer = Observer()
        event_handler = MyEventHandler()
        self.observer.schedule(event_handler, path, recursive=True)

    def streamingOn(self) -> None:
        self.observer.start()

    # Streaming Off + Send Data
    def streamingOff(self) -> None:
        self.observer.stop()
