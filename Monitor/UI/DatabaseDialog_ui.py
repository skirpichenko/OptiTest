# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatabaseDialog.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableView, QVBoxLayout, QWidget)

class Ui_DatabaseDialog(object):
    def setupUi(self, DatabaseDialog):
        if not DatabaseDialog.objectName():
            DatabaseDialog.setObjectName(u"DatabaseDialog")
        DatabaseDialog.resize(750, 450)
        self.gridLayout_2 = QGridLayout(DatabaseDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(DatabaseDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(True)
        self.tabSubstrate = QWidget()
        self.tabSubstrate.setObjectName(u"tabSubstrate")
        self.horizontalLayout_2 = QHBoxLayout(self.tabSubstrate)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tableViewSubstrate = QTableView(self.tabSubstrate)
        self.tableViewSubstrate.setObjectName(u"tableViewSubstrate")
        self.tableViewSubstrate.setFrameShape(QFrame.NoFrame)
        self.tableViewSubstrate.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout_2.addWidget(self.tableViewSubstrate)

        self.tabWidgetSubstrate = QTabWidget(self.tabSubstrate)
        self.tabWidgetSubstrate.setObjectName(u"tabWidgetSubstrate")
        self.tabWidgetSubstrate.setTabPosition(QTabWidget.South)
        self.tabPlotSubstrate = QWidget()
        self.tabPlotSubstrate.setObjectName(u"tabPlotSubstrate")
        self.tabWidgetSubstrate.addTab(self.tabPlotSubstrate, "")
        self.tabData = QWidget()
        self.tabData.setObjectName(u"tabData")
        self.horizontalLayout_4 = QHBoxLayout(self.tabData)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableViewSubstrateMaterial = QTableView(self.tabData)
        self.tableViewSubstrateMaterial.setObjectName(u"tableViewSubstrateMaterial")
        self.tableViewSubstrateMaterial.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_4.addWidget(self.tableViewSubstrateMaterial)

        self.tabWidgetSubstrate.addTab(self.tabData, "")

        self.horizontalLayout_2.addWidget(self.tabWidgetSubstrate)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.tabWidget.addTab(self.tabSubstrate, "")
        self.tabLayerMaterial = QWidget()
        self.tabLayerMaterial.setObjectName(u"tabLayerMaterial")
        self.horizontalLayout_3 = QHBoxLayout(self.tabLayerMaterial)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tableViewLayerMaterial = QTableView(self.tabLayerMaterial)
        self.tableViewLayerMaterial.setObjectName(u"tableViewLayerMaterial")
        self.tableViewLayerMaterial.setFrameShape(QFrame.NoFrame)
        self.tableViewLayerMaterial.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout_3.addWidget(self.tableViewLayerMaterial)

        self.tabWidgetLayerMaterial = QTabWidget(self.tabLayerMaterial)
        self.tabWidgetLayerMaterial.setObjectName(u"tabWidgetLayerMaterial")
        self.tabWidgetLayerMaterial.setTabPosition(QTabWidget.South)
        self.tabPlotLayerMaterial = QWidget()
        self.tabPlotLayerMaterial.setObjectName(u"tabPlotLayerMaterial")
        self.tabWidgetLayerMaterial.addTab(self.tabPlotLayerMaterial, "")
        self.tabData1 = QWidget()
        self.tabData1.setObjectName(u"tabData1")
        self.horizontalLayout_5 = QHBoxLayout(self.tabData1)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.tableViewLayerMaterialMaterial = QTableView(self.tabData1)
        self.tableViewLayerMaterialMaterial.setObjectName(u"tableViewLayerMaterialMaterial")
        self.tableViewLayerMaterialMaterial.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_5.addWidget(self.tableViewLayerMaterialMaterial)

        self.tabWidgetLayerMaterial.addTab(self.tabData1, "")

        self.horizontalLayout_3.addWidget(self.tabWidgetLayerMaterial)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)
        self.tabWidget.addTab(self.tabLayerMaterial, "")
        self.tabDesign = QWidget()
        self.tabDesign.setObjectName(u"tabDesign")
        self.verticalLayout = QVBoxLayout(self.tabDesign)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.tabDesign)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEditNumberOfLayers = QLineEdit(self.tabDesign)
        self.lineEditNumberOfLayers.setObjectName(u"lineEditNumberOfLayers")
        self.lineEditNumberOfLayers.setFrame(False)
        self.lineEditNumberOfLayers.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditNumberOfLayers, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(198, 108, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 4, 1)

        self.label_3 = QLabel(self.tabDesign)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.lineEditDesignWavelength = QLineEdit(self.tabDesign)
        self.lineEditDesignWavelength.setObjectName(u"lineEditDesignWavelength")
        self.lineEditDesignWavelength.setFrame(False)
        self.lineEditDesignWavelength.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditDesignWavelength, 1, 1, 1, 1)

        self.label_4 = QLabel(self.tabDesign)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEditAngelOfIncidence = QLineEdit(self.tabDesign)
        self.lineEditAngelOfIncidence.setObjectName(u"lineEditAngelOfIncidence")
        self.lineEditAngelOfIncidence.setFrame(False)
        self.lineEditAngelOfIncidence.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditAngelOfIncidence, 2, 1, 1, 1)

        self.label_5 = QLabel(self.tabDesign)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.lineEditInputMedium = QLineEdit(self.tabDesign)
        self.lineEditInputMedium.setObjectName(u"lineEditInputMedium")
        self.lineEditInputMedium.setFrame(False)
        self.lineEditInputMedium.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditInputMedium, 3, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 150)
        self.gridLayout.setColumnStretch(2, 255)

        self.verticalLayout.addLayout(self.gridLayout)

        self.label = QLabel(self.tabDesign)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tableViewDesign = QTableView(self.tabDesign)
        self.tableViewDesign.setObjectName(u"tableViewDesign")
        self.tableViewDesign.setFrameShape(QFrame.NoFrame)
        self.tableViewDesign.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableViewDesign)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButtonOk = QPushButton(self.tabDesign)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)

        self.pushButtonCancel = QPushButton(self.tabDesign)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tabDesign, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

#if QT_CONFIG(shortcut)
        self.label_2.setBuddy(self.lineEditNumberOfLayers)
        self.label_3.setBuddy(self.lineEditDesignWavelength)
        self.label_4.setBuddy(self.lineEditAngelOfIncidence)
        self.label_5.setBuddy(self.lineEditInputMedium)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(DatabaseDialog)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidgetSubstrate.setCurrentIndex(0)
        self.tabWidgetLayerMaterial.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DatabaseDialog)
    # setupUi

    def retranslateUi(self, DatabaseDialog):
        DatabaseDialog.setWindowTitle(QCoreApplication.translate("DatabaseDialog", u"Database", None))
        self.tabWidgetSubstrate.setTabText(self.tabWidgetSubstrate.indexOf(self.tabPlotSubstrate), QCoreApplication.translate("DatabaseDialog", u"Plot", None))
        self.tabWidgetSubstrate.setTabText(self.tabWidgetSubstrate.indexOf(self.tabData), QCoreApplication.translate("DatabaseDialog", u"Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSubstrate), QCoreApplication.translate("DatabaseDialog", u"Substrate", None))
        self.tabWidgetLayerMaterial.setTabText(self.tabWidgetLayerMaterial.indexOf(self.tabPlotLayerMaterial), QCoreApplication.translate("DatabaseDialog", u"Plot", None))
        self.tabWidgetLayerMaterial.setTabText(self.tabWidgetLayerMaterial.indexOf(self.tabData1), QCoreApplication.translate("DatabaseDialog", u"Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLayerMaterial), QCoreApplication.translate("DatabaseDialog", u"Layer Material", None))
        self.label_2.setText(QCoreApplication.translate("DatabaseDialog", u"The number of layers = ", None))
        self.label_3.setText(QCoreApplication.translate("DatabaseDialog", u"Design wavelength (nm) = ", None))
        self.label_4.setText(QCoreApplication.translate("DatabaseDialog", u"Angle of incidence (deg) =", None))
        self.label_5.setText(QCoreApplication.translate("DatabaseDialog", u"Input medium = ", None))
        self.label.setText(QCoreApplication.translate("DatabaseDialog", u"Speedsheet", None))
        self.pushButtonOk.setText(QCoreApplication.translate("DatabaseDialog", u"OK", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("DatabaseDialog", u"Cancel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDesign), QCoreApplication.translate("DatabaseDialog", u"Design", None))
    # retranslateUi

