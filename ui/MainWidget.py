# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.setFixedSize(800, 220)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.dirLabel = QLabel(Form)
        self.dirLabel.setObjectName("dirLabel")
        self.dirLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.dirLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.browseDirBtn = QPushButton(Form)
        self.browseDirBtn.setObjectName("browseDirBtn")

        self.horizontalLayout.addWidget(self.browseDirBtn)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toggleBtn = QPushButton(Form)
        self.toggleBtn.setObjectName("toggleBtn")

        self.horizontalLayout.addWidget(self.toggleBtn)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.logTextBrowser = QTextBrowser(Form)
        self.logTextBrowser.setObjectName("logTextBrowser")

        self.verticalLayout.addWidget(self.logTextBrowser)

        self.statusLabel = QLabel(Form)
        self.statusLabel.setObjectName("statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.dirLabel.setText(
            QCoreApplication.translate("Form", "Selected Directory : None", None)
        )
        self.browseDirBtn.setText(
            QCoreApplication.translate("Form", "Browse Directory", None)
        )
        self.toggleBtn.setText(
            QCoreApplication.translate("Form", "Start Observer", None)
        )
        self.logTextBrowser.setHtml(
            QCoreApplication.translate(
                "Form",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "hr { height: 1px; border-width: 0; }\n"
                'li.unchecked::marker { content: "\\2610"; }\n'
                'li.checked::marker { content: "\\2612"; }\n'
                "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Log will be displayed here.</p></body></html>',
                None,
            )
        )
        self.statusLabel.setText(
            QCoreApplication.translate("Form", "Status : Not Running", None)
        )

    # retranslateUi
