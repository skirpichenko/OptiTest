# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainLogDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainLogDialog(object):
    def setupUi(self, MainLogDialog):
        if not MainLogDialog.objectName():
            MainLogDialog.setObjectName(u"MainLogDialog")
        MainLogDialog.resize(640, 480)
        self.verticalLayout = QVBoxLayout(MainLogDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 0)
        self.checkBoxAutoscroll = QCheckBox(MainLogDialog)
        self.checkBoxAutoscroll.setObjectName(u"checkBoxAutoscroll")
        self.checkBoxAutoscroll.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBoxAutoscroll)

        self.pushButtonClear = QPushButton(MainLogDialog)
        self.pushButtonClear.setObjectName(u"pushButtonClear")
        self.pushButtonClear.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pushButtonClear)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.plainTextEdit = QPlainTextEdit(MainLogDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)


        self.retranslateUi(MainLogDialog)

        QMetaObject.connectSlotsByName(MainLogDialog)
    # setupUi

    def retranslateUi(self, MainLogDialog):
        MainLogDialog.setWindowTitle(QCoreApplication.translate("MainLogDialog", u"Log", None))
        self.checkBoxAutoscroll.setText(QCoreApplication.translate("MainLogDialog", u"Autoscroll", None))
        self.pushButtonClear.setText(QCoreApplication.translate("MainLogDialog", u"Clear", None))
    # retranslateUi

