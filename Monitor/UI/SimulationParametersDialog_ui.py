# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SimulationParametersDialog.ui'
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
    QDialogButtonBox, QDoubleSpinBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QRadioButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)

class Ui_SimulationParametersDialog(object):
    def setupUi(self, SimulationParametersDialog):
        if not SimulationParametersDialog.objectName():
            SimulationParametersDialog.setObjectName(u"SimulationParametersDialog")
        SimulationParametersDialog.resize(806, 514)
        self.verticalLayout_13 = QVBoxLayout(SimulationParametersDialog)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tableView = QTableView(SimulationParametersDialog)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_13.addWidget(self.tableView)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBoxRefining = QGroupBox(SimulationParametersDialog)
        self.groupBoxRefining.setObjectName(u"groupBoxRefining")
        self.verticalLayout = QVBoxLayout(self.groupBoxRefining)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioButtonRefiningLastLayer = QRadioButton(self.groupBoxRefining)
        self.radioButtonRefiningLastLayer.setObjectName(u"radioButtonRefiningLastLayer")

        self.verticalLayout.addWidget(self.radioButtonRefiningLastLayer)

        self.radioButtonRefiningAllLayers = QRadioButton(self.groupBoxRefining)
        self.radioButtonRefiningAllLayers.setObjectName(u"radioButtonRefiningAllLayers")

        self.verticalLayout.addWidget(self.radioButtonRefiningAllLayers)


        self.horizontalLayout_3.addWidget(self.groupBoxRefining)

        self.groupBox_2 = QGroupBox(SimulationParametersDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(24)
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.doubleSpinBoxWavelengthLimitsLower = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBoxWavelengthLimitsLower.setObjectName(u"doubleSpinBoxWavelengthLimitsLower")
        self.doubleSpinBoxWavelengthLimitsLower.setDecimals(3)

        self.gridLayout.addWidget(self.doubleSpinBoxWavelengthLimitsLower, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.doubleSpinBoxWavelengthLimitsUpper = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBoxWavelengthLimitsUpper.setObjectName(u"doubleSpinBoxWavelengthLimitsUpper")
        self.doubleSpinBoxWavelengthLimitsUpper.setDecimals(3)

        self.gridLayout.addWidget(self.doubleSpinBoxWavelengthLimitsUpper, 1, 1, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox_2)


        self.verticalLayout_11.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 26, -1, 16)
        self.label_3 = QLabel(SimulationParametersDialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_7.addWidget(self.label_3)

        self.doubleSpinBoxRandomErrors = QDoubleSpinBox(SimulationParametersDialog)
        self.doubleSpinBoxRandomErrors.setObjectName(u"doubleSpinBoxRandomErrors")
        self.doubleSpinBoxRandomErrors.setDecimals(3)
        self.doubleSpinBoxRandomErrors.setMaximum(100.000000000000000)

        self.verticalLayout_7.addWidget(self.doubleSpinBoxRandomErrors)

        self.label_4 = QLabel(SimulationParametersDialog)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_7.addWidget(self.label_4)

        self.doubleSpinBoxMeanShutterDelay = QDoubleSpinBox(SimulationParametersDialog)
        self.doubleSpinBoxMeanShutterDelay.setObjectName(u"doubleSpinBoxMeanShutterDelay")
        self.doubleSpinBoxMeanShutterDelay.setDecimals(3)

        self.verticalLayout_7.addWidget(self.doubleSpinBoxMeanShutterDelay)

        self.label_5 = QLabel(SimulationParametersDialog)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_7.addWidget(self.label_5)

        self.doubleSpinBoxShutterDelayRMS = QDoubleSpinBox(SimulationParametersDialog)
        self.doubleSpinBoxShutterDelayRMS.setObjectName(u"doubleSpinBoxShutterDelayRMS")
        self.doubleSpinBoxShutterDelayRMS.setDecimals(3)

        self.verticalLayout_7.addWidget(self.doubleSpinBoxShutterDelayRMS)


        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.groupBox_3 = QGroupBox(SimulationParametersDialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_3.addWidget(self.label_6)

        self.doubleSpinBoxFluktuationsDrift = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxFluktuationsDrift.setObjectName(u"doubleSpinBoxFluktuationsDrift")
        self.doubleSpinBoxFluktuationsDrift.setDecimals(3)
        self.doubleSpinBoxFluktuationsDrift.setMaximum(100.000000000000000)

        self.verticalLayout_3.addWidget(self.doubleSpinBoxFluktuationsDrift)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.doubleSpinBoxFluktuationsMeanTime = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxFluktuationsMeanTime.setObjectName(u"doubleSpinBoxFluktuationsMeanTime")
        self.doubleSpinBoxFluktuationsMeanTime.setDecimals(3)

        self.verticalLayout_3.addWidget(self.doubleSpinBoxFluktuationsMeanTime)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_3.addWidget(self.label_8)

        self.doubleSpinBoxFluktuationsRMS = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxFluktuationsRMS.setObjectName(u"doubleSpinBoxFluktuationsRMS")
        self.doubleSpinBoxFluktuationsRMS.setDecimals(3)

        self.verticalLayout_3.addWidget(self.doubleSpinBoxFluktuationsRMS)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(SimulationParametersDialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_2.addWidget(self.label_9)

        self.doubleSpinBoxCalibrationDriftsRate = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBoxCalibrationDriftsRate.setObjectName(u"doubleSpinBoxCalibrationDriftsRate")
        self.doubleSpinBoxCalibrationDriftsRate.setDecimals(3)

        self.verticalLayout_2.addWidget(self.doubleSpinBoxCalibrationDriftsRate)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_2.addWidget(self.label_10)

        self.doubleSpinBoxCalibrationDriftsRecalibrTime = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBoxCalibrationDriftsRecalibrTime.setObjectName(u"doubleSpinBoxCalibrationDriftsRecalibrTime")
        self.doubleSpinBoxCalibrationDriftsRecalibrTime.setDecimals(3)

        self.verticalLayout_2.addWidget(self.doubleSpinBoxCalibrationDriftsRecalibrTime)

        self.verticalSpacer = QSpacerItem(20, 46, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addWidget(self.groupBox_4)


        self.verticalLayout_11.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 8, -1, -1)
        self.groupBox_5 = QGroupBox(SimulationParametersDialog)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_6.addWidget(self.label_11)

        self.doubleSpinBoxAngleOfIncidence = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBoxAngleOfIncidence.setObjectName(u"doubleSpinBoxAngleOfIncidence")
        self.doubleSpinBoxAngleOfIncidence.setDecimals(3)
        self.doubleSpinBoxAngleOfIncidence.setMaximum(89.998999999999995)

        self.verticalLayout_6.addWidget(self.doubleSpinBoxAngleOfIncidence)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)


        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.groupBox_6 = QGroupBox(self.groupBox_5)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setFlat(False)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radioButtonPOL_S = QRadioButton(self.groupBox_6)
        self.radioButtonPOL_S.setObjectName(u"radioButtonPOL_S")

        self.verticalLayout_4.addWidget(self.radioButtonPOL_S)

        self.radioButtonPOL_P = QRadioButton(self.groupBox_6)
        self.radioButtonPOL_P.setObjectName(u"radioButtonPOL_P")

        self.verticalLayout_4.addWidget(self.radioButtonPOL_P)

        self.radioButtonPOL_A = QRadioButton(self.groupBox_6)
        self.radioButtonPOL_A.setObjectName(u"radioButtonPOL_A")

        self.verticalLayout_4.addWidget(self.radioButtonPOL_A)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)


        self.horizontalLayout.addWidget(self.groupBox_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_5.addWidget(self.label_12)

        self.doubleSpinBoxScanInterval = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBoxScanInterval.setObjectName(u"doubleSpinBoxScanInterval")
        self.doubleSpinBoxScanInterval.setDecimals(3)
        self.doubleSpinBoxScanInterval.setValue(2.000000000000000)

        self.verticalLayout_5.addWidget(self.doubleSpinBoxScanInterval)

        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_5.addWidget(self.label_13)

        self.comboBoxTimeBetweenScans = QComboBox(self.groupBox_5)
        self.comboBoxTimeBetweenScans.addItem("")
        self.comboBoxTimeBetweenScans.addItem("")
        self.comboBoxTimeBetweenScans.addItem("")
        self.comboBoxTimeBetweenScans.addItem("")
        self.comboBoxTimeBetweenScans.addItem("")
        self.comboBoxTimeBetweenScans.addItem("")
        self.comboBoxTimeBetweenScans.addItem("")
        self.comboBoxTimeBetweenScans.setObjectName(u"comboBoxTimeBetweenScans")

        self.verticalLayout_5.addWidget(self.comboBoxTimeBetweenScans)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)


        self.horizontalLayout.addLayout(self.verticalLayout_5)


        self.verticalLayout_12.addWidget(self.groupBox_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_7 = QGroupBox(SimulationParametersDialog)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.radioButtonInputData_Transmittance = QRadioButton(self.groupBox_7)
        self.radioButtonInputData_Transmittance.setObjectName(u"radioButtonInputData_Transmittance")

        self.verticalLayout_9.addWidget(self.radioButtonInputData_Transmittance)

        self.radioButtonInputData_Reflectance = QRadioButton(self.groupBox_7)
        self.radioButtonInputData_Reflectance.setObjectName(u"radioButtonInputData_Reflectance")

        self.verticalLayout_9.addWidget(self.radioButtonInputData_Reflectance)


        self.horizontalLayout_4.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(SimulationParametersDialog)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.radioButtonInputDataShift_Shift = QRadioButton(self.groupBox_8)
        self.radioButtonInputDataShift_Shift.setObjectName(u"radioButtonInputDataShift_Shift")

        self.verticalLayout_10.addWidget(self.radioButtonInputDataShift_Shift)

        self.radioButtonInputDataShift_Scale = QRadioButton(self.groupBox_8)
        self.radioButtonInputDataShift_Scale.setObjectName(u"radioButtonInputDataShift_Scale")

        self.verticalLayout_10.addWidget(self.radioButtonInputDataShift_Scale)


        self.horizontalLayout_4.addWidget(self.groupBox_8)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_14 = QLabel(SimulationParametersDialog)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_8.addWidget(self.label_14)

        self.doubleSpinBoxThOfTheSubstrate = QDoubleSpinBox(SimulationParametersDialog)
        self.doubleSpinBoxThOfTheSubstrate.setObjectName(u"doubleSpinBoxThOfTheSubstrate")
        self.doubleSpinBoxThOfTheSubstrate.setDecimals(3)

        self.verticalLayout_8.addWidget(self.doubleSpinBoxThOfTheSubstrate)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_7)


        self.horizontalLayout_4.addLayout(self.verticalLayout_8)


        self.verticalLayout_12.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_12)


        self.verticalLayout_13.addLayout(self.horizontalLayout_5)

        self.buttonBox = QDialogButtonBox(SimulationParametersDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_13.addWidget(self.buttonBox)

        self.verticalLayout_13.setStretch(0, 255)
        self.verticalLayout_13.setStretch(1, 1)
        self.verticalLayout_13.setStretch(2, 1)

        self.retranslateUi(SimulationParametersDialog)
        self.buttonBox.accepted.connect(SimulationParametersDialog.accept)
        self.buttonBox.rejected.connect(SimulationParametersDialog.reject)

        self.comboBoxTimeBetweenScans.setCurrentIndex(6)


        QMetaObject.connectSlotsByName(SimulationParametersDialog)
    # setupUi

    def retranslateUi(self, SimulationParametersDialog):
        SimulationParametersDialog.setWindowTitle(QCoreApplication.translate("SimulationParametersDialog", u"Simulation Parameters", None))
        self.groupBoxRefining.setTitle(QCoreApplication.translate("SimulationParametersDialog", u"Refining", None))
        self.radioButtonRefiningLastLayer.setText(QCoreApplication.translate("SimulationParametersDialog", u"Only last layer", None))
        self.radioButtonRefiningAllLayers.setText(QCoreApplication.translate("SimulationParametersDialog", u"All layers", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SimulationParametersDialog", u"Wavelength limits:", None))
        self.label_2.setText(QCoreApplication.translate("SimulationParametersDialog", u"Upper wavelength", None))
        self.label.setText(QCoreApplication.translate("SimulationParametersDialog", u"Lower wavelength", None))
        self.label_3.setText(QCoreApplication.translate("SimulationParametersDialog", u"Random errors (%)", None))
        self.label_4.setText(QCoreApplication.translate("SimulationParametersDialog", u"Mean shutter delay (s)", None))
        self.label_5.setText(QCoreApplication.translate("SimulationParametersDialog", u"Shutter delay RMS (s)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SimulationParametersDialog", u"Fluktuations", None))
        self.label_6.setText(QCoreApplication.translate("SimulationParametersDialog", u"Drift (%)", None))
        self.label_7.setText(QCoreApplication.translate("SimulationParametersDialog", u"Mean time (s)", None))
        self.label_8.setText(QCoreApplication.translate("SimulationParametersDialog", u"RMS (s)", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("SimulationParametersDialog", u"Calibration drifts", None))
        self.label_9.setText(QCoreApplication.translate("SimulationParametersDialog", u"Rate, %./1000s", None))
        self.label_10.setText(QCoreApplication.translate("SimulationParametersDialog", u"Recalibr. time (s)", None))
        self.groupBox_5.setTitle("")
        self.label_11.setText(QCoreApplication.translate("SimulationParametersDialog", u"Angle of incidence", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("SimulationParametersDialog", u"Polarization state", None))
        self.radioButtonPOL_S.setText(QCoreApplication.translate("SimulationParametersDialog", u"POL_S", None))
        self.radioButtonPOL_P.setText(QCoreApplication.translate("SimulationParametersDialog", u"POL_P", None))
        self.radioButtonPOL_A.setText(QCoreApplication.translate("SimulationParametersDialog", u"POL_A", None))
        self.label_12.setText(QCoreApplication.translate("SimulationParametersDialog", u"Scan interval (s)", None))
        self.label_13.setText(QCoreApplication.translate("SimulationParametersDialog", u"Time between scans", None))
        self.comboBoxTimeBetweenScans.setItemText(0, QCoreApplication.translate("SimulationParametersDialog", u"Normal", None))
        self.comboBoxTimeBetweenScans.setItemText(1, QCoreApplication.translate("SimulationParametersDialog", u"Normal / 2", None))
        self.comboBoxTimeBetweenScans.setItemText(2, QCoreApplication.translate("SimulationParametersDialog", u"Normal / 4", None))
        self.comboBoxTimeBetweenScans.setItemText(3, QCoreApplication.translate("SimulationParametersDialog", u"Normal / 8", None))
        self.comboBoxTimeBetweenScans.setItemText(4, QCoreApplication.translate("SimulationParametersDialog", u"Normal / 16", None))
        self.comboBoxTimeBetweenScans.setItemText(5, QCoreApplication.translate("SimulationParametersDialog", u"Normal / 32", None))
        self.comboBoxTimeBetweenScans.setItemText(6, QCoreApplication.translate("SimulationParametersDialog", u"No delay (maximum prefix)", None))

        self.groupBox_7.setTitle(QCoreApplication.translate("SimulationParametersDialog", u"Input data", None))
        self.radioButtonInputData_Transmittance.setText(QCoreApplication.translate("SimulationParametersDialog", u"Transmittance", None))
        self.radioButtonInputData_Reflectance.setText(QCoreApplication.translate("SimulationParametersDialog", u"Reflectance", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("SimulationParametersDialog", u"Input data shift", None))
        self.radioButtonInputDataShift_Shift.setText(QCoreApplication.translate("SimulationParametersDialog", u"Shift", None))
        self.radioButtonInputDataShift_Scale.setText(QCoreApplication.translate("SimulationParametersDialog", u"Scale", None))
        self.label_14.setText(QCoreApplication.translate("SimulationParametersDialog", u"Th. of the substrate (nm)", None))
    # retranslateUi

