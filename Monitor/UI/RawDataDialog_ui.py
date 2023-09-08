# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RawDataDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
                               QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
                               QWidget)


class Ui_RawDataDialog(object):
    def setupUi(self, RawDataDialog):
        if not RawDataDialog.objectName():
            RawDataDialog.setObjectName(u"RawDataDialog")
        RawDataDialog.resize(640, 334)
        self.verticalLayout = QVBoxLayout(RawDataDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frameChartView = QFrame(RawDataDialog)
        self.frameChartView.setObjectName(u"frameChartView")
        self.frameChartView.setFrameShape(QFrame.StyledPanel)
        self.frameChartView.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frameChartView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, 2, 2)
        self.horizontalSpacer = QSpacerItem(518, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonExportToCsv = QPushButton(RawDataDialog)
        self.pushButtonExportToCsv.setObjectName(u"pushButtonExportToCsv")
        self.pushButtonExportToCsv.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pushButtonExportToCsv)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(0, 255)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(RawDataDialog)

        QMetaObject.connectSlotsByName(RawDataDialog)

    # setupUi

    def retranslateUi(self, RawDataDialog):
        RawDataDialog.setWindowTitle(QCoreApplication.translate("RawDataDialog", u"Raw Data", None))
        self.pushButtonExportToCsv.setText(QCoreApplication.translate("RawDataDialog", u"Export to CSV", None))
    # retranslateUi
