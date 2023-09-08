# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HistoryDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QListView,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_HistoryDialog(object):
    def setupUi(self, HistoryDialog):
        if not HistoryDialog.objectName():
            HistoryDialog.setObjectName(u"HistoryDialog")
        HistoryDialog.resize(436, 500)
        self.verticalLayout = QVBoxLayout(HistoryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listViewHistory = QListView(HistoryDialog)
        self.listViewHistory.setObjectName(u"listViewHistory")

        self.verticalLayout.addWidget(self.listViewHistory)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOpen = QPushButton(HistoryDialog)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")

        self.horizontalLayout.addWidget(self.pushButtonOpen)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(HistoryDialog)

        QMetaObject.connectSlotsByName(HistoryDialog)
    # setupUi

    def retranslateUi(self, HistoryDialog):
        HistoryDialog.setWindowTitle(QCoreApplication.translate("HistoryDialog", u"History", None))
        self.pushButtonOpen.setText(QCoreApplication.translate("HistoryDialog", u"Open data fitting for selected item", None))
    # retranslateUi

