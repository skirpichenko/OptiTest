# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProcessParametersDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_ProcessParametersDialog(object):
    def setupUi(self, ProcessParametersDialog):
        if not ProcessParametersDialog.objectName():
            ProcessParametersDialog.setObjectName(u"ProcessParametersDialog")
        ProcessParametersDialog.resize(516, 470)
        self.verticalLayout_5 = QVBoxLayout(ProcessParametersDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBoxRefining = QGroupBox(ProcessParametersDialog)
        self.groupBoxRefining.setObjectName(u"groupBoxRefining")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxRefining)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButtonRefiningLast = QRadioButton(self.groupBoxRefining)
        self.radioButtonRefiningLast.setObjectName(u"radioButtonRefiningLast")

        self.verticalLayout_2.addWidget(self.radioButtonRefiningLast)

        self.radioButtonRefiningAll = QRadioButton(self.groupBoxRefining)
        self.radioButtonRefiningAll.setObjectName(u"radioButtonRefiningAll")

        self.verticalLayout_2.addWidget(self.radioButtonRefiningAll)


        self.horizontalLayout_4.addWidget(self.groupBoxRefining)

        self.groupBoxWavelengthLimits = QGroupBox(ProcessParametersDialog)
        self.groupBoxWavelengthLimits.setObjectName(u"groupBoxWavelengthLimits")
        self.gridLayout_2 = QGridLayout(self.groupBoxWavelengthLimits)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.groupBoxWavelengthLimits)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_7 = QLabel(self.groupBoxWavelengthLimits)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 1, 1, 1)

        self.lineEditLowerWavelength = QLineEdit(self.groupBoxWavelengthLimits)
        self.lineEditLowerWavelength.setObjectName(u"lineEditLowerWavelength")

        self.gridLayout_2.addWidget(self.lineEditLowerWavelength, 1, 0, 1, 1)

        self.lineEditUpperWavelength = QLineEdit(self.groupBoxWavelengthLimits)
        self.lineEditUpperWavelength.setObjectName(u"lineEditUpperWavelength")

        self.gridLayout_2.addWidget(self.lineEditUpperWavelength, 1, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.groupBoxWavelengthLimits)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBoxPalarizationState = QGroupBox(ProcessParametersDialog)
        self.groupBoxPalarizationState.setObjectName(u"groupBoxPalarizationState")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxPalarizationState)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.radioButtonPOL_S = QRadioButton(self.groupBoxPalarizationState)
        self.radioButtonPOL_S.setObjectName(u"radioButtonPOL_S")

        self.verticalLayout_3.addWidget(self.radioButtonPOL_S)

        self.radioButtonPOL_P = QRadioButton(self.groupBoxPalarizationState)
        self.radioButtonPOL_P.setObjectName(u"radioButtonPOL_P")

        self.verticalLayout_3.addWidget(self.radioButtonPOL_P)

        self.radioButtonPOL_A = QRadioButton(self.groupBoxPalarizationState)
        self.radioButtonPOL_A.setObjectName(u"radioButtonPOL_A")

        self.verticalLayout_3.addWidget(self.radioButtonPOL_A)


        self.horizontalLayout_5.addWidget(self.groupBoxPalarizationState)

        self.groupBox_4 = QGroupBox(ProcessParametersDialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout = QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBoxMaterials = QComboBox(self.groupBox_4)
        self.comboBoxMaterials.setObjectName(u"comboBoxMaterials")

        self.gridLayout.addWidget(self.comboBoxMaterials, 1, 2, 1, 1)

        self.lineEditMeanShutterDelay = QLineEdit(self.groupBox_4)
        self.lineEditMeanShutterDelay.setObjectName(u"lineEditMeanShutterDelay")

        self.gridLayout.addWidget(self.lineEditMeanShutterDelay, 1, 3, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(308, 36, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 2, 0, 1, 4)

        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 2)

        self.lineEditAngleOfIncidence = QLineEdit(self.groupBox_4)
        self.lineEditAngleOfIncidence.setObjectName(u"lineEditAngleOfIncidence")

        self.gridLayout.addWidget(self.lineEditAngleOfIncidence, 1, 0, 1, 2)

        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 1)

        self.horizontalLayout_5.addWidget(self.groupBox_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBoxInputData = QGroupBox(ProcessParametersDialog)
        self.groupBoxInputData.setObjectName(u"groupBoxInputData")
        self.horizontalLayout = QHBoxLayout(self.groupBoxInputData)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButtonTransmittance = QRadioButton(self.groupBoxInputData)
        self.radioButtonTransmittance.setObjectName(u"radioButtonTransmittance")

        self.horizontalLayout.addWidget(self.radioButtonTransmittance)

        self.radioButtonReflectance = QRadioButton(self.groupBoxInputData)
        self.radioButtonReflectance.setObjectName(u"radioButtonReflectance")

        self.horizontalLayout.addWidget(self.radioButtonReflectance)


        self.horizontalLayout_6.addWidget(self.groupBoxInputData)

        self.groupBoxInputDataShift = QGroupBox(ProcessParametersDialog)
        self.groupBoxInputDataShift.setObjectName(u"groupBoxInputDataShift")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBoxInputDataShift)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButtonShift = QRadioButton(self.groupBoxInputDataShift)
        self.radioButtonShift.setObjectName(u"radioButtonShift")

        self.horizontalLayout_2.addWidget(self.radioButtonShift)

        self.radioButtonScale = QRadioButton(self.groupBoxInputDataShift)
        self.radioButtonScale.setObjectName(u"radioButtonScale")

        self.horizontalLayout_2.addWidget(self.radioButtonScale)


        self.horizontalLayout_6.addWidget(self.groupBoxInputDataShift)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 9, -1)
        self.label = QLabel(ProcessParametersDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.lineEditThOfSubstrate = QLineEdit(ProcessParametersDialog)
        self.lineEditThOfSubstrate.setObjectName(u"lineEditThOfSubstrate")

        self.verticalLayout_4.addWidget(self.lineEditThOfSubstrate)


        self.horizontalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.groupBoxReoptimization = QGroupBox(ProcessParametersDialog)
        self.groupBoxReoptimization.setObjectName(u"groupBoxReoptimization")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBoxReoptimization)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBoxEnableReoptimization = QCheckBox(self.groupBoxReoptimization)
        self.checkBoxEnableReoptimization.setObjectName(u"checkBoxEnableReoptimization")

        self.horizontalLayout_3.addWidget(self.checkBoxEnableReoptimization)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_2 = QLabel(self.groupBoxReoptimization)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(False)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(self.groupBoxReoptimization)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(False)

        self.gridLayout_3.addWidget(self.label_3, 0, 1, 1, 1)

        self.lineEditLowerReoptimization = QLineEdit(self.groupBoxReoptimization)
        self.lineEditLowerReoptimization.setObjectName(u"lineEditLowerReoptimization")
        self.lineEditLowerReoptimization.setEnabled(False)

        self.gridLayout_3.addWidget(self.lineEditLowerReoptimization, 1, 0, 1, 1)

        self.lineEditUpperReoptimization = QLineEdit(self.groupBoxReoptimization)
        self.lineEditUpperReoptimization.setObjectName(u"lineEditUpperReoptimization")
        self.lineEditUpperReoptimization.setEnabled(False)

        self.gridLayout_3.addWidget(self.lineEditUpperReoptimization, 1, 1, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_3)


        self.verticalLayout_5.addWidget(self.groupBoxReoptimization)

        self.groupBoxExtra = QGroupBox(ProcessParametersDialog)
        self.groupBoxExtra.setObjectName(u"groupBoxExtra")
        self.verticalLayout = QVBoxLayout(self.groupBoxExtra)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBoxCreateBinaryLog = QCheckBox(self.groupBoxExtra)
        self.checkBoxCreateBinaryLog.setObjectName(u"checkBoxCreateBinaryLog")

        self.verticalLayout.addWidget(self.checkBoxCreateBinaryLog)


        self.verticalLayout_5.addWidget(self.groupBoxExtra)

        self.verticalSpacer = QSpacerItem(498, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ProcessParametersDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_5.addWidget(self.buttonBox)

        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 1)
        self.verticalLayout_5.setStretch(2, 1)
        self.verticalLayout_5.setStretch(3, 1)
        self.verticalLayout_5.setStretch(4, 1)
        self.verticalLayout_5.setStretch(5, 255)
        self.verticalLayout_5.setStretch(6, 1)
        QWidget.setTabOrder(self.radioButtonRefiningLast, self.radioButtonRefiningAll)
        QWidget.setTabOrder(self.radioButtonRefiningAll, self.lineEditLowerWavelength)
        QWidget.setTabOrder(self.lineEditLowerWavelength, self.radioButtonPOL_S)
        QWidget.setTabOrder(self.radioButtonPOL_S, self.radioButtonPOL_P)
        QWidget.setTabOrder(self.radioButtonPOL_P, self.radioButtonPOL_A)
        QWidget.setTabOrder(self.radioButtonPOL_A, self.lineEditAngleOfIncidence)
        QWidget.setTabOrder(self.lineEditAngleOfIncidence, self.radioButtonTransmittance)
        QWidget.setTabOrder(self.radioButtonTransmittance, self.radioButtonReflectance)
        QWidget.setTabOrder(self.radioButtonReflectance, self.radioButtonShift)
        QWidget.setTabOrder(self.radioButtonShift, self.radioButtonScale)
        QWidget.setTabOrder(self.radioButtonScale, self.lineEditThOfSubstrate)
        QWidget.setTabOrder(self.lineEditThOfSubstrate, self.checkBoxEnableReoptimization)
        QWidget.setTabOrder(self.checkBoxEnableReoptimization, self.lineEditLowerReoptimization)
        QWidget.setTabOrder(self.lineEditLowerReoptimization, self.lineEditUpperReoptimization)
        QWidget.setTabOrder(self.lineEditUpperReoptimization, self.checkBoxCreateBinaryLog)

        self.retranslateUi(ProcessParametersDialog)
        self.buttonBox.accepted.connect(ProcessParametersDialog.accept)
        self.buttonBox.rejected.connect(ProcessParametersDialog.reject)
        self.checkBoxEnableReoptimization.clicked["bool"].connect(self.lineEditLowerReoptimization.setEnabled)
        self.checkBoxEnableReoptimization.clicked["bool"].connect(self.lineEditUpperReoptimization.setEnabled)
        self.checkBoxEnableReoptimization.clicked["bool"].connect(self.label_2.setEnabled)
        self.checkBoxEnableReoptimization.clicked["bool"].connect(self.label_3.setEnabled)

        QMetaObject.connectSlotsByName(ProcessParametersDialog)
    # setupUi

    def retranslateUi(self, ProcessParametersDialog):
        ProcessParametersDialog.setWindowTitle(QCoreApplication.translate("ProcessParametersDialog", u"Process Parameters", None))
        self.groupBoxRefining.setTitle(QCoreApplication.translate("ProcessParametersDialog", u"Refining", None))
        self.radioButtonRefiningLast.setText(QCoreApplication.translate("ProcessParametersDialog", u"Only last layer", None))
        self.radioButtonRefiningAll.setText(QCoreApplication.translate("ProcessParametersDialog", u"All layers", None))
        self.groupBoxWavelengthLimits.setTitle(QCoreApplication.translate("ProcessParametersDialog", u"Wavelength Limits", None))
        self.label_6.setText(QCoreApplication.translate("ProcessParametersDialog", u"Lower wavelength", None))
        self.label_7.setText(QCoreApplication.translate("ProcessParametersDialog", u"Upper wavelength", None))
        self.groupBoxPalarizationState.setTitle(QCoreApplication.translate("ProcessParametersDialog", u"Polarization State", None))
        self.radioButtonPOL_S.setText(QCoreApplication.translate("ProcessParametersDialog", u"POL_S", None))
        self.radioButtonPOL_P.setText(QCoreApplication.translate("ProcessParametersDialog", u"POL_P", None))
        self.radioButtonPOL_A.setText(QCoreApplication.translate("ProcessParametersDialog", u"POL_A", None))
        self.groupBox_4.setTitle("")
        self.label_5.setText(QCoreApplication.translate("ProcessParametersDialog", u"Mean shutter delay (s)", None))
        self.label_4.setText(QCoreApplication.translate("ProcessParametersDialog", u"Angle of incidence", None))
        self.groupBoxInputData.setTitle(QCoreApplication.translate("ProcessParametersDialog", u"Input Data", None))
        self.radioButtonTransmittance.setText(QCoreApplication.translate("ProcessParametersDialog", u"Transmittance", None))
        self.radioButtonReflectance.setText(QCoreApplication.translate("ProcessParametersDialog", u"Reflectance", None))
        self.groupBoxInputDataShift.setTitle(QCoreApplication.translate("ProcessParametersDialog", u"Input Data Shift", None))
        self.radioButtonShift.setText(QCoreApplication.translate("ProcessParametersDialog", u"Shift", None))
        self.radioButtonScale.setText(QCoreApplication.translate("ProcessParametersDialog", u"Scale", None))
        self.label.setText(QCoreApplication.translate("ProcessParametersDialog", u"Th. of the substrate (mm)", None))
        self.groupBoxReoptimization.setTitle(QCoreApplication.translate("ProcessParametersDialog", u"Reoptimization", None))
        self.checkBoxEnableReoptimization.setText(QCoreApplication.translate("ProcessParametersDialog", u"Enable reoptimization", None))
        self.label_2.setText(QCoreApplication.translate("ProcessParametersDialog", u"Lower reopt. wavelength", None))
        self.label_3.setText(QCoreApplication.translate("ProcessParametersDialog", u"Upper reopt. wavelength", None))
        self.groupBoxExtra.setTitle(QCoreApplication.translate("ProcessParametersDialog", u"Extra", None))
        self.checkBoxCreateBinaryLog.setText(QCoreApplication.translate("ProcessParametersDialog", u"Create binary log", None))
    # retranslateUi

