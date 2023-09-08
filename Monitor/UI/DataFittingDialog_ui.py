# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataFittingDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHeaderView,
    QSizePolicy, QTabWidget, QTableView, QVBoxLayout,
    QWidget)

class Ui_DataFittingDialog(object):
    def setupUi(self, DataFittingDialog):
        if not DataFittingDialog.objectName():
            DataFittingDialog.setObjectName(u"DataFittingDialog")
        DataFittingDialog.resize(892, 374)
        self.verticalLayout = QVBoxLayout(DataFittingDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(DataFittingDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabSpectralDataFitting = QWidget()
        self.tabSpectralDataFitting.setObjectName(u"tabSpectralDataFitting")
        self.tabWidget.addTab(self.tabSpectralDataFitting, "")
        self.tabThicknesses = QWidget()
        self.tabThicknesses.setObjectName(u"tabThicknesses")
        self.verticalLayout_2 = QVBoxLayout(self.tabThicknesses)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidgetThicknesses = QTabWidget(self.tabThicknesses)
        self.tabWidgetThicknesses.setObjectName(u"tabWidgetThicknesses")
        self.tabWidgetThicknesses.setTabPosition(QTabWidget.South)
        self.tabWidgetThicknesses.setDocumentMode(True)
        self.tabRelativeErrors = QWidget()
        self.tabRelativeErrors.setObjectName(u"tabRelativeErrors")
        self.tabWidgetThicknesses.addTab(self.tabRelativeErrors, "")
        self.tabAbsoluteErrors = QWidget()
        self.tabAbsoluteErrors.setObjectName(u"tabAbsoluteErrors")
        self.tabWidgetThicknesses.addTab(self.tabAbsoluteErrors, "")
        self.tabTable = QWidget()
        self.tabTable.setObjectName(u"tabTable")
        self.verticalLayout_3 = QVBoxLayout(self.tabTable)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.thicknessTableView = QTableView(self.tabTable)
        self.thicknessTableView.setObjectName(u"thicknessTableView")
        self.thicknessTableView.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_3.addWidget(self.thicknessTableView)

        self.tabWidgetThicknesses.addTab(self.tabTable, "")

        self.verticalLayout_2.addWidget(self.tabWidgetThicknesses)

        self.tabWidget.addTab(self.tabThicknesses, "")
        self.tabRatesChart = QWidget()
        self.tabRatesChart.setObjectName(u"tabRatesChart")
        self.tabWidget.addTab(self.tabRatesChart, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(DataFittingDialog)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidgetThicknesses.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DataFittingDialog)
    # setupUi

    def retranslateUi(self, DataFittingDialog):
        DataFittingDialog.setWindowTitle(QCoreApplication.translate("DataFittingDialog", u"Data Fitting", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSpectralDataFitting), QCoreApplication.translate("DataFittingDialog", u"Spectral Data Fitting", None))
        self.tabWidgetThicknesses.setTabText(self.tabWidgetThicknesses.indexOf(self.tabRelativeErrors), QCoreApplication.translate("DataFittingDialog", u"Relative Errors", None))
        self.tabWidgetThicknesses.setTabText(self.tabWidgetThicknesses.indexOf(self.tabAbsoluteErrors), QCoreApplication.translate("DataFittingDialog", u"Absolute Errors", None))
        self.tabWidgetThicknesses.setTabText(self.tabWidgetThicknesses.indexOf(self.tabTable), QCoreApplication.translate("DataFittingDialog", u"Table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabThicknesses), QCoreApplication.translate("DataFittingDialog", u"Thicknesses", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRatesChart), QCoreApplication.translate("DataFittingDialog", u"Rates Chart", None))
    # retranslateUi

