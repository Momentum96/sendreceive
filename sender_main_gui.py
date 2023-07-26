import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PySide6.QtGui import QCloseEvent, QTextCursor, QIcon
from ui.MainWidget import Ui_Form
from utils.etc import observe
import logging
from datetime import datetime
import os

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class MyApp(QWidget, Ui_Form):
    def __init__(self) -> None:
        super(MyApp, self).__init__()
        self.setupUi(self)  # Inherited methods
        self.setupProperties()

        # Button Event
        self.browseDirBtn.clicked.connect(self.selectDirectory)
        self.toggleBtn.clicked.connect(self.startStreaming)

    # 번수, 컴포넌트 초기화
    def setupProperties(self) -> None:
        # Properties
        self.isStreaming = False
        self.isFirstDirectory = True

        # fixed dir
        self.dir = "C:\logs"
        self.dirLabel.setText("Dir : " + self.dir)
        self.browseDirBtn.setEnabled(False)
        # self.toggleBtn.setEnabled(False)

        # Componenets setting
        self.logTextBrowser.verticalScrollBar().setValue(
            self.logTextBrowser.verticalScrollBar().maximum()
        )
        self.logger = logging.getLogger()
        self.logger.addHandler(LogStringHandler(self.logTextBrowser))

        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "ui", "banf_icon.png")))

    # Browse Directory 버튼 클릭 이벤트
    def selectDirectory(self) -> None:
        if self.isFirstDirectory:
            self.logTextBrowser.setText("")
            self.isFirstDirectory = False

        self.dir = QFileDialog.getExistingDirectory()

        if self.dir == "":
            self.dirLabel.setText("Directory is not Selected.")
            self.setStatus("Directory Select Failed.")
        else:
            self.dirLabel.setText("Dir : " + self.dir)
            self.setStatus("Directory Selected.")
            self.toggleBtn.setEnabled(True)

    # Start Observer 버튼 클릭 이벤트
    def startStreaming(self) -> None:
        if not self.isStreaming:
            self.statusLabel.setStyleSheet("Color : green")
            # self.browseDirBtn.setEnabled(False)
            self.streamer = observe.FileObserver()
            self.streamer.setObserver(self.dir)
            self.streamer.streamingOn()
            self.toggleBtn.setText("Stop Observe")
            self.setStatus("Streaming Started.")
            self.isStreaming = True

        else:
            self.statusLabel.setStyleSheet("Color : red")
            # self.browseDirBtn.setEnabled(True)
            self.streamer.streamingOff()
            self.streamer = None
            self.toggleBtn.setText("Start Observe")
            self.setStatus("Streaming Stopped.")
            self.isStreaming = False

    # status 표시 및 logging
    def setStatus(self, text: str) -> None:
        self.statusLabel.setText("Status : " + text)
        logging.info("Status : " + text)

    def createDir(self, directory: str) -> None:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            self.setStatus("Error creating directory " + directory)

    # 창 종료 시 로그 저장을 위한 이벤트
    # def closeEvent(self, event: QCloseEvent) -> None:
    #     log = self.logTextBrowser.toPlainText()
    #     if log.count("\n") >= 2:
    #         self.createDir(
    #             os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    #         )
    #         f = open(
    #             "C:/logs/log_" + datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".txt",
    #             "w",
    #         )
    #         f.write(log)
    #         f.close()
            # event.accept() 조건에 따라 이벤트 종료, 무시(ignore) 설정 시 필요


# Log String을 text browser에 이어나가기 위함
class LogStringHandler(logging.Handler):  # Singleton Default
    def __init__(self, target_widget) -> None:
        super(LogStringHandler, self).__init__()
        self.target_widget = target_widget

    def emit(self, record) -> None:
        self.target_widget.append(record.asctime + " -- " + record.getMessage())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MyApp()
    main.show()

    sys.exit(app.exec())
