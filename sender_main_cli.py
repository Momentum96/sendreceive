from utils.etc import observe
import time
import logging

# logging.basicConfig(
#     filename="./sender-lte.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main():
    observing_dir = "C:/logs"

    streamer = observe.FileObserver()
    streamer.setObserver(observing_dir)
    streamer.streamingOn()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(1)
