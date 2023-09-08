# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SpectrometerSettingsDialog.ui'
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
    QDialog, QDialogButtonBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_SpectrometerSettingsDialog(object):
    def setupUi(self, SpectrometerSettingsDialog):
        if not SpectrometerSettingsDialog.objectName():
            SpectrometerSettingsDialog.setObjectName(u"SpectrometerSettingsDialog")
        SpectrometerSettingsDialog.resize(550, 500)
        self.verticalLayout_2 = QVBoxLayout(SpectrometerSettingsDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(SpectrometerSettingsDialog)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBoxSpectrometer = QComboBox(SpectrometerSettingsDialog)
        self.comboBoxSpectrometer.setObjectName(u"comboBoxSpectrometer")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comboBoxSpectrometer)


        self.horizontalLayout_3.addLayout(self.formLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 26, -1, -1)
        self.lineEditIntegrationTime = QLineEdit(SpectrometerSettingsDialog)
        self.lineEditIntegrationTime.setObjectName(u"lineEditIntegrationTime")

        self.gridLayout_2.addWidget(self.lineEditIntegrationTime, 1, 1, 1, 1)

        self.label_2 = QLabel(SpectrometerSettingsDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEditNumberOfScans = QLineEdit(SpectrometerSettingsDialog)
        self.lineEditNumberOfScans.setObjectName(u"lineEditNumberOfScans")

        self.gridLayout_2.addWidget(self.lineEditNumberOfScans, 0, 1, 1, 1)

        self.label_3 = QLabel(SpectrometerSettingsDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 2)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.groupBox = QGroupBox(SpectrometerSettingsDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_7)

        self.lineEditBroadBandSample = QLineEdit(self.groupBox)
        self.lineEditBroadBandSample.setObjectName(u"lineEditBroadBandSample")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEditBroadBandSample)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_8)

        self.lineEditBroadBandDark = QLineEdit(self.groupBox)
        self.lineEditBroadBandDark.setObjectName(u"lineEditBroadBandDark")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEditBroadBandDark)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_9)

        self.lineEditBroadBandReference = QLineEdit(self.groupBox)
        self.lineEditBroadBandReference.setObjectName(u"lineEditBroadBandReference")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEditBroadBandReference)


        self.gridLayout_3.addWidget(self.groupBox, 0, 1, 1, 1)

        self.groupBox_2 = QGroupBox(SpectrometerSettingsDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBoxSystemDialogSetup = QCheckBox(self.groupBox_2)
        self.checkBoxSystemDialogSetup.setObjectName(u"checkBoxSystemDialogSetup")

        self.verticalLayout.addWidget(self.checkBoxSystemDialogSetup)

        self.checkBoxSystemDialogMeasurements = QCheckBox(self.groupBox_2)
        self.checkBoxSystemDialogMeasurements.setObjectName(u"checkBoxSystemDialogMeasurements")

        self.verticalLayout.addWidget(self.checkBoxSystemDialogMeasurements)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 26, 9, -1)
        self.label_4 = QLabel(SpectrometerSettingsDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.lineEditMeasDelay = QLineEdit(SpectrometerSettingsDialog)
        self.lineEditMeasDelay.setObjectName(u"lineEditMeasDelay")

        self.gridLayout.addWidget(self.lineEditMeasDelay, 2, 1, 1, 1)

        self.lineEditOptiTrigPort = QLineEdit(SpectrometerSettingsDialog)
        self.lineEditOptiTrigPort.setObjectName(u"lineEditOptiTrigPort")

        self.gridLayout.addWidget(self.lineEditOptiTrigPort, 0, 1, 1, 1)

        self.checkBoxDetectNoiseInSpectra = QCheckBox(SpectrometerSettingsDialog)
        self.checkBoxDetectNoiseInSpectra.setObjectName(u"checkBoxDetectNoiseInSpectra")

        self.gridLayout.addWidget(self.checkBoxDetectNoiseInSpectra, 1, 1, 1, 1)

        self.label_5 = QLabel(SpectrometerSettingsDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.verticalSpacer_4 = QSpacerItem(498, 77, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.groupBox_3 = QGroupBox(SpectrometerSettingsDialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditRAWDataLogging = QLineEdit(self.groupBox_3)
        self.lineEditRAWDataLogging.setObjectName(u"lineEditRAWDataLogging")

        self.horizontalLayout.addWidget(self.lineEditRAWDataLogging)

        self.pushButtonRAWDataLoggingBrowse = QPushButton(self.groupBox_3)
        self.pushButtonRAWDataLoggingBrowse.setObjectName(u"pushButtonRAWDataLoggingBrowse")

        self.horizontalLayout.addWidget(self.pushButtonRAWDataLoggingBrowse)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_6 = QLabel(SpectrometerSettingsDialog)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.comboBoxFilter = QComboBox(SpectrometerSettingsDialog)
        self.comboBoxFilter.setObjectName(u"comboBoxFilter")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.comboBoxFilter)


        self.horizontalLayout_2.addLayout(self.formLayout_3)

        self.horizontalSpacer = QSpacerItem(208, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(SpectrometerSettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 255)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 1)
        self.verticalLayout_2.setStretch(5, 1)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.comboBoxSpectrometer)
        self.label_2.setBuddy(self.lineEditNumberOfScans)
        self.label_3.setBuddy(self.lineEditIntegrationTime)
        self.label_7.setBuddy(self.lineEditBroadBandSample)
        self.label_8.setBuddy(self.lineEditBroadBandDark)
        self.label_9.setBuddy(self.lineEditBroadBandReference)
        self.label_4.setBuddy(self.lineEditOptiTrigPort)
        self.label_5.setBuddy(self.lineEditMeasDelay)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(SpectrometerSettingsDialog)

        QMetaObject.connectSlotsByName(SpectrometerSettingsDialog)
    # setupUi

    def retranslateUi(self, SpectrometerSettingsDialog):
        SpectrometerSettingsDialog.setWindowTitle(QCoreApplication.translate("SpectrometerSettingsDialog", u"Spectrometer Settings", None))
        self.label.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Use the following spectrometer", None))
        self.label_2.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Number of scans", None))
        self.label_3.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Integration time", None))
        self.groupBox.setTitle(QCoreApplication.translate("SpectrometerSettingsDialog", u"BroadBand data order", None))
        self.label_7.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Sample", None))
        self.label_8.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Dark", None))
        self.label_9.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Reference", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SpectrometerSettingsDialog", u"System dialogs", None))
        self.checkBoxSystemDialogSetup.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Setup dialog", None))
        self.checkBoxSystemDialogMeasurements.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Measurements dialog", None))
        self.label_4.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"OptiTrig port", None))
        self.checkBoxDetectNoiseInSpectra.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Detect noise in spectra", None))
        self.label_5.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Meas. delay (ms)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SpectrometerSettingsDialog", u"RAW data logging", None))
        self.pushButtonRAWDataLoggingBrowse.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Browse...", None))
        self.label_6.setText(QCoreApplication.translate("SpectrometerSettingsDialog", u"Filter", None))
    # retranslateUi

