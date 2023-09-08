# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SpectrometerDataCorrectionDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_SpectrometerDataCorrectionDialog(object):
    def setupUi(self, SpectrometerDataCorrectionDialog):
        if not SpectrometerDataCorrectionDialog.objectName():
            SpectrometerDataCorrectionDialog.setObjectName(u"SpectrometerDataCorrectionDialog")
        SpectrometerDataCorrectionDialog.resize(800, 400)
        self.horizontalLayout_2 = QHBoxLayout(SpectrometerDataCorrectionDialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frameChart = QFrame(SpectrometerDataCorrectionDialog)
        self.frameChart.setObjectName(u"frameChart")
        self.frameChart.setFrameShape(QFrame.StyledPanel)
        self.frameChart.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frameChart)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SpectrometerDataCorrectionDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditMeasurementsCount = QLineEdit(SpectrometerDataCorrectionDialog)
        self.lineEditMeasurementsCount.setObjectName(u"lineEditMeasurementsCount")

        self.gridLayout.addWidget(self.lineEditMeasurementsCount, 0, 0, 1, 1)

        self.pushButtonCalcCoeff = QPushButton(SpectrometerDataCorrectionDialog)
        self.pushButtonCalcCoeff.setObjectName(u"pushButtonCalcCoeff")

        self.gridLayout.addWidget(self.pushButtonCalcCoeff, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(SpectrometerDataCorrectionDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.labelCurrentMeasurement = QLabel(SpectrometerDataCorrectionDialog)
        self.labelCurrentMeasurement.setObjectName(u"labelCurrentMeasurement")

        self.horizontalLayout.addWidget(self.labelCurrentMeasurement)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 255)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.pushButtonSaveAndUse = QPushButton(SpectrometerDataCorrectionDialog)
        self.pushButtonSaveAndUse.setObjectName(u"pushButtonSaveAndUse")

        self.gridLayout.addWidget(self.pushButtonSaveAndUse, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tableView = QTableView(SpectrometerDataCorrectionDialog)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 255)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 2)

        self.retranslateUi(SpectrometerDataCorrectionDialog)

        QMetaObject.connectSlotsByName(SpectrometerDataCorrectionDialog)
    # setupUi

    def retranslateUi(self, SpectrometerDataCorrectionDialog):
        SpectrometerDataCorrectionDialog.setWindowTitle(QCoreApplication.translate("SpectrometerDataCorrectionDialog", u"Spectrometer Data Correction", None))
        self.label.setText(QCoreApplication.translate("SpectrometerDataCorrectionDialog", u"Measurements count", None))
        self.pushButtonCalcCoeff.setText(QCoreApplication.translate("SpectrometerDataCorrectionDialog", u"Calc. coeff.", None))
        self.label_2.setText(QCoreApplication.translate("SpectrometerDataCorrectionDialog", u"Current measurement:", None))
        self.labelCurrentMeasurement.setText(QCoreApplication.translate("SpectrometerDataCorrectionDialog", u"n/a", None))
        self.pushButtonSaveAndUse.setText(QCoreApplication.translate("SpectrometerDataCorrectionDialog", u"Save and use", None))
    # retranslateUi

