# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ErrorPreventionDuringDepositionDialog.ui'
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
    QDialog, QDialogButtonBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ErrorPreventionDuringDepositionDialog(object):
    def setupUi(self, ErrorPreventionDuringDepositionDialog):
        if not ErrorPreventionDuringDepositionDialog.objectName():
            ErrorPreventionDuringDepositionDialog.setObjectName(u"ErrorPreventionDuringDepositionDialog")
        ErrorPreventionDuringDepositionDialog.resize(691, 95)
        self.verticalLayout = QVBoxLayout(ErrorPreventionDuringDepositionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBoxStopProcess = QCheckBox(ErrorPreventionDuringDepositionDialog)
        self.checkBoxStopProcess.setObjectName(u"checkBoxStopProcess")
        self.checkBoxStopProcess.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBoxStopProcess)

        self.comboBoxLessEqualMore = QComboBox(ErrorPreventionDuringDepositionDialog)
        self.comboBoxLessEqualMore.addItem("")
        self.comboBoxLessEqualMore.addItem("")
        self.comboBoxLessEqualMore.addItem("")
        self.comboBoxLessEqualMore.addItem("")
        self.comboBoxLessEqualMore.addItem("")
        self.comboBoxLessEqualMore.setObjectName(u"comboBoxLessEqualMore")

        self.horizontalLayout.addWidget(self.comboBoxLessEqualMore)

        self.lineEditFrom = QLineEdit(ErrorPreventionDuringDepositionDialog)
        self.lineEditFrom.setObjectName(u"lineEditFrom")

        self.horizontalLayout.addWidget(self.lineEditFrom)

        self.label = QLabel(ErrorPreventionDuringDepositionDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditTo = QLineEdit(ErrorPreventionDuringDepositionDialog)
        self.lineEditTo.setObjectName(u"lineEditTo")

        self.horizontalLayout.addWidget(self.lineEditTo)

        self.label_2 = QLabel(ErrorPreventionDuringDepositionDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ErrorPreventionDuringDepositionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ErrorPreventionDuringDepositionDialog)
        self.buttonBox.accepted.connect(ErrorPreventionDuringDepositionDialog.accept)
        self.buttonBox.rejected.connect(ErrorPreventionDuringDepositionDialog.reject)
        self.checkBoxStopProcess.clicked["bool"].connect(self.comboBoxLessEqualMore.setEnabled)
        self.checkBoxStopProcess.clicked["bool"].connect(self.lineEditFrom.setEnabled)
        self.checkBoxStopProcess.clicked["bool"].connect(self.lineEditTo.setEnabled)

        QMetaObject.connectSlotsByName(ErrorPreventionDuringDepositionDialog)
    # setupUi

    def retranslateUi(self, ErrorPreventionDuringDepositionDialog):
        ErrorPreventionDuringDepositionDialog.setWindowTitle(QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"Error Prevention During Deposition", None))
        self.checkBoxStopProcess.setText(QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"Stop process if the \"Rate\" variable is", None))
        self.comboBoxLessEqualMore.setItemText(0, QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"less than", None))
        self.comboBoxLessEqualMore.setItemText(1, QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"less or equal to", None))
        self.comboBoxLessEqualMore.setItemText(2, QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"equal to", None))
        self.comboBoxLessEqualMore.setItemText(3, QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"more or equal to", None))
        self.comboBoxLessEqualMore.setItemText(4, QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"more than", None))

        self.label.setText(QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"(A/s) during", None))
        self.label_2.setText(QCoreApplication.translate("ErrorPreventionDuringDepositionDialog", u"consecutive measurements", None))
    # retranslateUi

