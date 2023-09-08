# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VacuumMachineSettngsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_VacuumMachineSettngsDialog(object):
    def setupUi(self, VacuumMachineSettngsDialog):
        if not VacuumMachineSettngsDialog.objectName():
            VacuumMachineSettngsDialog.setObjectName(u"VacuumMachineSettngsDialog")
        VacuumMachineSettngsDialog.resize(460, 230)
        self.gridLayout_2 = QGridLayout(VacuumMachineSettngsDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(VacuumMachineSettngsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(VacuumMachineSettngsDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBoxVacuumMachine = QComboBox(VacuumMachineSettngsDialog)
        self.comboBoxVacuumMachine.addItem("")
        self.comboBoxVacuumMachine.addItem("")
        self.comboBoxVacuumMachine.addItem("")
        self.comboBoxVacuumMachine.addItem("")
        self.comboBoxVacuumMachine.setObjectName(u"comboBoxVacuumMachine")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBoxVacuumMachine)


        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(VacuumMachineSettngsDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageVirtual = QWidget()
        self.pageVirtual.setObjectName(u"pageVirtual")
        self.verticalLayout = QVBoxLayout(self.pageVirtual)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelVirtualInfo = QLabel(self.pageVirtual)
        self.labelVirtualInfo.setObjectName(u"labelVirtualInfo")
        self.labelVirtualInfo.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.labelVirtualInfo)

        self.stackedWidget.addWidget(self.pageVirtual)
        self.pageVPT = QWidget()
        self.pageVPT.setObjectName(u"pageVPT")
        self.gridLayout = QGridLayout(self.pageVPT)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditVPTUpdateRate = QLineEdit(self.pageVPT)
        self.lineEditVPTUpdateRate.setObjectName(u"lineEditVPTUpdateRate")

        self.gridLayout.addWidget(self.lineEditVPTUpdateRate, 1, 1, 1, 1)

        self.labelOPCServer = QLabel(self.pageVPT)
        self.labelOPCServer.setObjectName(u"labelOPCServer")
        self.labelOPCServer.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelOPCServer, 0, 0, 1, 1)

        self.labelUpdateRate = QLabel(self.pageVPT)
        self.labelUpdateRate.setObjectName(u"labelUpdateRate")
        self.labelUpdateRate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelUpdateRate, 1, 0, 1, 1)

        self.labelDelayBetweenLayers = QLabel(self.pageVPT)
        self.labelDelayBetweenLayers.setObjectName(u"labelDelayBetweenLayers")
        self.labelDelayBetweenLayers.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelayBetweenLayers, 2, 0, 1, 1)

        self.label_5 = QLabel(self.pageVPT)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)

        self.comboBoxVPTOPCServer = QComboBox(self.pageVPT)
        self.comboBoxVPTOPCServer.setObjectName(u"comboBoxVPTOPCServer")

        self.gridLayout.addWidget(self.comboBoxVPTOPCServer, 0, 1, 1, 2)

        self.lineEditVPTDelayBetweenLayers = QLineEdit(self.pageVPT)
        self.lineEditVPTDelayBetweenLayers.setObjectName(u"lineEditVPTDelayBetweenLayers")

        self.gridLayout.addWidget(self.lineEditVPTDelayBetweenLayers, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 3)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 255)
        self.gridLayout.setColumnStretch(2, 255)
        self.stackedWidget.addWidget(self.pageVPT)
        self.pageOptotech = QWidget()
        self.pageOptotech.setObjectName(u"pageOptotech")
        self.gridLayout_3 = QGridLayout(self.pageOptotech)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 4, 0, 1, 5)

        self.label_6 = QLabel(self.pageOptotech)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)

        self.lineEditOptotechDelayBetweenLayers = QLineEdit(self.pageOptotech)
        self.lineEditOptotechDelayBetweenLayers.setObjectName(u"lineEditOptotechDelayBetweenLayers")

        self.gridLayout_3.addWidget(self.lineEditOptotechDelayBetweenLayers, 2, 1, 1, 1)

        self.pushButtonOptotechDebugConsole = QPushButton(self.pageOptotech)
        self.pushButtonOptotechDebugConsole.setObjectName(u"pushButtonOptotechDebugConsole")

        self.gridLayout_3.addWidget(self.pushButtonOptotechDebugConsole, 1, 4, 1, 1)

        self.label_2 = QLabel(self.pageOptotech)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEditLocalPort = QLineEdit(self.pageOptotech)
        self.lineEditLocalPort.setObjectName(u"lineEditLocalPort")

        self.gridLayout_3.addWidget(self.lineEditLocalPort, 1, 1, 1, 1)

        self.lineEditOptotechConnectIPAdress = QLineEdit(self.pageOptotech)
        self.lineEditOptotechConnectIPAdress.setObjectName(u"lineEditOptotechConnectIPAdress")

        self.gridLayout_3.addWidget(self.lineEditOptotechConnectIPAdress, 0, 1, 1, 1)

        self.labelOptotechLoactPort = QLabel(self.pageOptotech)
        self.labelOptotechLoactPort.setObjectName(u"labelOptotechLoactPort")
        self.labelOptotechLoactPort.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.labelOptotechLoactPort, 1, 0, 1, 1)

        self.label_4 = QLabel(self.pageOptotech)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEditOptotechPort = QLineEdit(self.pageOptotech)
        self.lineEditOptotechPort.setObjectName(u"lineEditOptotechPort")

        self.gridLayout_3.addWidget(self.lineEditOptotechPort, 0, 4, 1, 1)

        self.label_9 = QLabel(self.pageOptotech)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_9, 0, 3, 1, 1)

        self.lineEditOptotechDataCorrectionCycles = QLineEdit(self.pageOptotech)
        self.lineEditOptotechDataCorrectionCycles.setObjectName(u"lineEditOptotechDataCorrectionCycles")

        self.gridLayout_3.addWidget(self.lineEditOptotechDataCorrectionCycles, 3, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 1, 2, 1, 2)

        self.label_7 = QLabel(self.pageOptotech)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 2, 2, 1, 3)

        self.label_8 = QLabel(self.pageOptotech)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 3, 2, 1, 3)

        self.stackedWidget.addWidget(self.pageOptotech)
        self.pageHSGroup = QWidget()
        self.pageHSGroup.setObjectName(u"pageHSGroup")
        self.gridLayout_4 = QGridLayout(self.pageHSGroup)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.lineEditHSGroupDelayBetweenLayers = QLineEdit(self.pageHSGroup)
        self.lineEditHSGroupDelayBetweenLayers.setObjectName(u"lineEditHSGroupDelayBetweenLayers")

        self.gridLayout_4.addWidget(self.lineEditHSGroupDelayBetweenLayers, 4, 1, 1, 1)

        self.comboBoxHSGroupOPCServer = QComboBox(self.pageHSGroup)
        self.comboBoxHSGroupOPCServer.setObjectName(u"comboBoxHSGroupOPCServer")

        self.gridLayout_4.addWidget(self.comboBoxHSGroupOPCServer, 1, 1, 1, 2)

        self.label_14 = QLabel(self.pageHSGroup)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_4.addWidget(self.label_14, 3, 2, 1, 1)

        self.label_11 = QLabel(self.pageHSGroup)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_11, 2, 0, 1, 1)

        self.lineEditHSGroupUpdateRate = QLineEdit(self.pageHSGroup)
        self.lineEditHSGroupUpdateRate.setObjectName(u"lineEditHSGroupUpdateRate")

        self.gridLayout_4.addWidget(self.lineEditHSGroupUpdateRate, 2, 1, 1, 1)

        self.label_12 = QLabel(self.pageHSGroup)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_12, 3, 0, 1, 1)

        self.label_3 = QLabel(self.pageHSGroup)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEditHSGroupRemoteComputerName = QLineEdit(self.pageHSGroup)
        self.lineEditHSGroupRemoteComputerName.setObjectName(u"lineEditHSGroupRemoteComputerName")

        self.gridLayout_4.addWidget(self.lineEditHSGroupRemoteComputerName, 0, 1, 1, 1)

        self.lineEditHSGroupOPCTagsPrefix = QLineEdit(self.pageHSGroup)
        self.lineEditHSGroupOPCTagsPrefix.setObjectName(u"lineEditHSGroupOPCTagsPrefix")

        self.gridLayout_4.addWidget(self.lineEditHSGroupOPCTagsPrefix, 3, 1, 1, 1)

        self.label_13 = QLabel(self.pageHSGroup)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 4, 2, 1, 1)

        self.label_15 = QLabel(self.pageHSGroup)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_15, 4, 0, 1, 1)

        self.label_10 = QLabel(self.pageHSGroup)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 5, 1, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 255)
        self.gridLayout_4.setColumnStretch(2, 255)
        self.stackedWidget.addWidget(self.pageHSGroup)

        self.gridLayout_2.addWidget(self.stackedWidget, 1, 0, 1, 1)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.comboBoxVacuumMachine)
        self.labelOPCServer.setBuddy(self.comboBoxVPTOPCServer)
        self.labelUpdateRate.setBuddy(self.lineEditVPTUpdateRate)
        self.labelDelayBetweenLayers.setBuddy(self.lineEditVPTDelayBetweenLayers)
        self.label_6.setBuddy(self.lineEditOptotechDataCorrectionCycles)
        self.label_2.setBuddy(self.lineEditOptotechConnectIPAdress)
        self.labelOptotechLoactPort.setBuddy(self.lineEditLocalPort)
        self.label_4.setBuddy(self.lineEditOptotechDelayBetweenLayers)
        self.label_9.setBuddy(self.lineEditOptotechPort)
        self.label_7.setBuddy(self.lineEditOptotechDelayBetweenLayers)
        self.label_8.setBuddy(self.lineEditOptotechDataCorrectionCycles)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(VacuumMachineSettngsDialog)
        self.buttonBox.accepted.connect(VacuumMachineSettngsDialog.accept)
        self.buttonBox.rejected.connect(VacuumMachineSettngsDialog.reject)
        self.comboBoxVacuumMachine.currentIndexChanged.connect(self.stackedWidget.setCurrentIndex)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(VacuumMachineSettngsDialog)
    # setupUi

    def retranslateUi(self, VacuumMachineSettngsDialog):
        VacuumMachineSettngsDialog.setWindowTitle(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Vacuum Machine Settngs", None))
        self.label.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Use the following vacuum machine", None))
        self.comboBoxVacuumMachine.setItemText(0, QCoreApplication.translate("VacuumMachineSettngsDialog", u"Virtual", None))
        self.comboBoxVacuumMachine.setItemText(1, QCoreApplication.translate("VacuumMachineSettngsDialog", u"VPT (OPC)", None))
        self.comboBoxVacuumMachine.setItemText(2, QCoreApplication.translate("VacuumMachineSettngsDialog", u"Optotech (TCP/IP)", None))
        self.comboBoxVacuumMachine.setItemText(3, QCoreApplication.translate("VacuumMachineSettngsDialog", u"HS-Group (OPC)", None))

        self.labelVirtualInfo.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"There are no settings available for this Vacuum Machine.", None))
        self.labelOPCServer.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"OPC server", None))
        self.labelUpdateRate.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Update rate (s)", None))
        self.labelDelayBetweenLayers.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Delay between layers (s)", None))
        self.label_5.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"* for debug only", None))
        self.label_6.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Data correction cycles", None))
        self.pushButtonOptotechDebugConsole.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Debug console", None))
        self.label_2.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Connect ro IP adress", None))
        self.labelOptotechLoactPort.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Local port", None))
        self.label_4.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Delay between layers (s)", None))
        self.label_9.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Port", None))
        self.label_7.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"* for debug only", None))
        self.label_8.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"* recommended value: 64", None))
        self.label_14.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"* app restart required ", None))
        self.label_11.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Update rate (s)", None))
        self.label_12.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"OPC tags prefix", None))
        self.label_3.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Remote computer name", None))
        self.label_13.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"* for debug only", None))
        self.label_15.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"Delay between layers (s)", None))
        self.label_10.setText(QCoreApplication.translate("VacuumMachineSettngsDialog", u"OPC servet", None))
    # retranslateUi

