# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProjectsDialog.ui'
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
    QListView, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ProjectsDialog(object):
    def setupUi(self, ProjectsDialog):
        if not ProjectsDialog.objectName():
            ProjectsDialog.setObjectName(u"ProjectsDialog")
        ProjectsDialog.resize(394, 428)
        self.verticalLayout = QVBoxLayout(ProjectsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelProjectsDirectory = QLabel(ProjectsDialog)
        self.labelProjectsDirectory.setObjectName(u"labelProjectsDirectory")

        self.horizontalLayout_2.addWidget(self.labelProjectsDirectory)

        self.pushButtonBrowse = QPushButton(ProjectsDialog)
        self.pushButtonBrowse.setObjectName(u"pushButtonBrowse")
        self.pushButtonBrowse.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.pushButtonBrowse)

        self.horizontalLayout_2.setStretch(0, 255)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listViewProjects = QListView(ProjectsDialog)
        self.listViewProjects.setObjectName(u"listViewProjects")

        self.verticalLayout.addWidget(self.listViewProjects)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButtonOpenProjectInExplorer = QPushButton(ProjectsDialog)
        self.pushButtonOpenProjectInExplorer.setObjectName(u"pushButtonOpenProjectInExplorer")
        self.pushButtonOpenProjectInExplorer.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pushButtonOpenProjectInExplorer)

        self.pushButtonCreateProject = QPushButton(ProjectsDialog)
        self.pushButtonCreateProject.setObjectName(u"pushButtonCreateProject")
        self.pushButtonCreateProject.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pushButtonCreateProject)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ProjectsDialog)

        QMetaObject.connectSlotsByName(ProjectsDialog)
    # setupUi

    def retranslateUi(self, ProjectsDialog):
        ProjectsDialog.setWindowTitle(QCoreApplication.translate("ProjectsDialog", u"Projects", None))
        self.labelProjectsDirectory.setText("")
        self.pushButtonBrowse.setText(QCoreApplication.translate("ProjectsDialog", u"Browse", None))
        self.pushButtonOpenProjectInExplorer.setText(QCoreApplication.translate("ProjectsDialog", u"Open current project in explorer", None))
        self.pushButtonCreateProject.setText(QCoreApplication.translate("ProjectsDialog", u"Create new project from LMR file", None))
    # retranslateUi

