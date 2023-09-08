# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'IterationExecutionTimeDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QListView, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_IterationExecutionTimeDialog(object):
    def setupUi(self, IterationExecutionTimeDialog):
        if not IterationExecutionTimeDialog.objectName():
            IterationExecutionTimeDialog.setObjectName(u"IterationExecutionTimeDialog")
        IterationExecutionTimeDialog.resize(350, 450)
        self.horizontalLayout = QHBoxLayout(IterationExecutionTimeDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(IterationExecutionTimeDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.listViewIterationExecTime = QListView(IterationExecutionTimeDialog)
        self.listViewIterationExecTime.setObjectName(u"listViewIterationExecTime")

        self.verticalLayout_2.addWidget(self.listViewIterationExecTime)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(IterationExecutionTimeDialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.lineEditOptiReCalculationTime = QLineEdit(IterationExecutionTimeDialog)
        self.lineEditOptiReCalculationTime.setObjectName(u"lineEditOptiReCalculationTime")

        self.verticalLayout.addWidget(self.lineEditOptiReCalculationTime)

        self.label_3 = QLabel(IterationExecutionTimeDialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.lineEditDepositionTime = QLineEdit(IterationExecutionTimeDialog)
        self.lineEditDepositionTime.setObjectName(u"lineEditDepositionTime")

        self.verticalLayout.addWidget(self.lineEditDepositionTime)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 255)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(IterationExecutionTimeDialog)

        QMetaObject.connectSlotsByName(IterationExecutionTimeDialog)
    # setupUi

    def retranslateUi(self, IterationExecutionTimeDialog):
        IterationExecutionTimeDialog.setWindowTitle(QCoreApplication.translate("IterationExecutionTimeDialog", u"Iteration Execution Time ", None))
        self.label.setText(QCoreApplication.translate("IterationExecutionTimeDialog", u"Iteration execution time (sec)", None))
        self.label_2.setText(QCoreApplication.translate("IterationExecutionTimeDialog", u"OptiRe Calculation Time ", None))
        self.label_3.setText(QCoreApplication.translate("IterationExecutionTimeDialog", u"Deposition Time", None))
    # retranslateUi

