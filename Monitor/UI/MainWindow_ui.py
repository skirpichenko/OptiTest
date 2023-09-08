# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(924, 552)
        self.actionProjects = QAction(MainWindow)
        self.actionProjects.setObjectName(u"actionProjects")
        self.actionSubstrate = QAction(MainWindow)
        self.actionSubstrate.setObjectName(u"actionSubstrate")
        self.actionLayerMaterial = QAction(MainWindow)
        self.actionLayerMaterial.setObjectName(u"actionLayerMaterial")
        self.actionDesign = QAction(MainWindow)
        self.actionDesign.setObjectName(u"actionDesign")
        self.actionProcessParameters = QAction(MainWindow)
        self.actionProcessParameters.setObjectName(u"actionProcessParameters")
        self.actionDataFitting = QAction(MainWindow)
        self.actionDataFitting.setObjectName(u"actionDataFitting")
        self.actionHistory = QAction(MainWindow)
        self.actionHistory.setObjectName(u"actionHistory")
        self.actionIterationExecutionTime = QAction(MainWindow)
        self.actionIterationExecutionTime.setObjectName(u"actionIterationExecutionTime")
        self.actionSaveSpectra = QAction(MainWindow)
        self.actionSaveSpectra.setObjectName(u"actionSaveSpectra")
        self.actionSaveSpectra.setCheckable(True)
        self.actionSimulationParameters = QAction(MainWindow)
        self.actionSimulationParameters.setObjectName(u"actionSimulationParameters")
        self.actionReverseEngineering = QAction(MainWindow)
        self.actionReverseEngineering.setObjectName(u"actionReverseEngineering")
        self.actionSpectrometerSettings = QAction(MainWindow)
        self.actionSpectrometerSettings.setObjectName(u"actionSpectrometerSettings")
        self.actionDataCorrection = QAction(MainWindow)
        self.actionDataCorrection.setObjectName(u"actionDataCorrection")
        self.actionRawData = QAction(MainWindow)
        self.actionRawData.setObjectName(u"actionRawData")
        self.actionMainLog = QAction(MainWindow)
        self.actionMainLog.setObjectName(u"actionMainLog")
        self.actionVacuumMachineSettings = QAction(MainWindow)
        self.actionVacuumMachineSettings.setObjectName(u"actionVacuumMachineSettings")
        self.actionErrorPrevention = QAction(MainWindow)
        self.actionErrorPrevention.setObjectName(u"actionErrorPrevention")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionImportSubstrate = QAction(MainWindow)
        self.actionImportSubstrate.setObjectName(u"actionImportSubstrate")
        self.actionImportMaterialL = QAction(MainWindow)
        self.actionImportMaterialL.setObjectName(u"actionImportMaterialL")
        self.actionImportMaterialH = QAction(MainWindow)
        self.actionImportMaterialH.setObjectName(u"actionImportMaterialH")
        self.actionImportDesign = QAction(MainWindow)
        self.actionImportDesign.setObjectName(u"actionImportDesign")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_chart = QFrame(self.centralwidget)
        self.frame_chart.setObjectName(u"frame_chart")
        self.frame_chart.setFrameShape(QFrame.StyledPanel)
        self.frame_chart.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frame_chart)

        self.frame_operations = QFrame(self.centralwidget)
        self.frame_operations.setObjectName(u"frame_operations")
        self.frame_operations.setFrameShape(QFrame.StyledPanel)
        self.frame_operations.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_operations)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_operations = QGroupBox(self.frame_operations)
        self.groupBox_operations.setObjectName(u"groupBox_operations")
        self.horizontalLayout = QHBoxLayout(self.groupBox_operations)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonStart = QPushButton(self.groupBox_operations)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStart.sizePolicy().hasHeightForWidth())
        self.pushButtonStart.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButtonStart)

        self.pushButtonReset = QPushButton(self.groupBox_operations)
        self.pushButtonReset.setObjectName(u"pushButtonReset")
        sizePolicy.setHeightForWidth(self.pushButtonReset.sizePolicy().hasHeightForWidth())
        self.pushButtonReset.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButtonReset)


        self.horizontalLayout_2.addWidget(self.groupBox_operations)

        self.groupBox_information = QGroupBox(self.frame_operations)
        self.groupBox_information.setObjectName(u"groupBox_information")
        self.gridLayout = QGridLayout(self.groupBox_information)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox_information)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditDesignTh = QLineEdit(self.groupBox_information)
        self.lineEditDesignTh.setObjectName(u"lineEditDesignTh")
        self.lineEditDesignTh.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditDesignTh, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_information)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.lineEditCurrentTh = QLineEdit(self.groupBox_information)
        self.lineEditCurrentTh.setObjectName(u"lineEditCurrentTh")
        self.lineEditCurrentTh.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditCurrentTh, 0, 3, 1, 1)

        self.label_7 = QLabel(self.groupBox_information)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 0, 4, 1, 1)

        self.lineEditValueF_Av = QLineEdit(self.groupBox_information)
        self.lineEditValueF_Av.setObjectName(u"lineEditValueF_Av")
        self.lineEditValueF_Av.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditValueF_Av, 0, 5, 1, 1)

        self.label_9 = QLabel(self.groupBox_information)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 0, 6, 1, 1)

        self.lineEditRemTh = QLineEdit(self.groupBox_information)
        self.lineEditRemTh.setObjectName(u"lineEditRemTh")
        self.lineEditRemTh.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditRemTh, 0, 7, 1, 1)

        self.label_2 = QLabel(self.groupBox_information)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEditActiveLayer = QLineEdit(self.groupBox_information)
        self.lineEditActiveLayer.setObjectName(u"lineEditActiveLayer")
        self.lineEditActiveLayer.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditActiveLayer, 1, 1, 1, 1)

        self.labelRate = QLabel(self.groupBox_information)
        self.labelRate.setObjectName(u"labelRate")
        self.labelRate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelRate, 1, 2, 1, 1)

        self.lineEditRate = QLineEdit(self.groupBox_information)
        self.lineEditRate.setObjectName(u"lineEditRate")
        self.lineEditRate.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditRate, 1, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox_information)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_8, 1, 4, 1, 1)

        self.lineEditExecutionT = QLineEdit(self.groupBox_information)
        self.lineEditExecutionT.setObjectName(u"lineEditExecutionT")
        self.lineEditExecutionT.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditExecutionT, 1, 5, 1, 1)

        self.label_10 = QLabel(self.groupBox_information)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 1, 6, 1, 1)

        self.lineEditMaterial = QLineEdit(self.groupBox_information)
        self.lineEditMaterial.setObjectName(u"lineEditMaterial")
        self.lineEditMaterial.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditMaterial, 1, 7, 1, 1)

        self.labelTotalLayers = QLabel(self.groupBox_information)
        self.labelTotalLayers.setObjectName(u"labelTotalLayers")
        self.labelTotalLayers.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelTotalLayers, 2, 0, 1, 1)

        self.lineEditTotalLayers = QLineEdit(self.groupBox_information)
        self.lineEditTotalLayers.setObjectName(u"lineEditTotalLayers")
        self.lineEditTotalLayers.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditTotalLayers, 2, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_information)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)

        self.lineEditRemTime = QLineEdit(self.groupBox_information)
        self.lineEditRemTime.setObjectName(u"lineEditRemTime")
        self.lineEditRemTime.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditRemTime, 2, 3, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_information)


        self.verticalLayout.addWidget(self.frame_operations)

        self.verticalLayout.setStretch(0, 255)
        self.verticalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 924, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuImport = QMenu(self.menuFile)
        self.menuImport.setObjectName(u"menuImport")
        self.menuDesign = QMenu(self.menubar)
        self.menuDesign.setObjectName(u"menuDesign")
        self.menuD_eposition_settings = QMenu(self.menubar)
        self.menuD_eposition_settings.setObjectName(u"menuD_eposition_settings")
        self.menu_Process_data = QMenu(self.menubar)
        self.menu_Process_data.setObjectName(u"menu_Process_data")
        self.menu_Spectrometer = QMenu(self.menubar)
        self.menu_Spectrometer.setObjectName(u"menu_Spectrometer")
        self.menu_Options = QMenu(self.menubar)
        self.menu_Options.setObjectName(u"menu_Options")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.lineEditDesignTh)
        self.label_4.setBuddy(self.lineEditCurrentTh)
        self.label_7.setBuddy(self.lineEditValueF_Av)
        self.label_9.setBuddy(self.lineEditRemTh)
        self.label_2.setBuddy(self.lineEditActiveLayer)
        self.labelRate.setBuddy(self.lineEditRate)
        self.label_8.setBuddy(self.lineEditExecutionT)
        self.label_10.setBuddy(self.lineEditMaterial)
        self.labelTotalLayers.setBuddy(self.lineEditTotalLayers)
        self.label_6.setBuddy(self.lineEditRemTime)
#endif // QT_CONFIG(shortcut)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDesign.menuAction())
        self.menubar.addAction(self.menuD_eposition_settings.menuAction())
        self.menubar.addAction(self.menu_Process_data.menuAction())
        self.menubar.addAction(self.menu_Spectrometer.menuAction())
        self.menubar.addAction(self.menu_Options.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addAction(self.actionProjects)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuImport.addAction(self.actionImportSubstrate)
        self.menuImport.addAction(self.actionImportMaterialL)
        self.menuImport.addAction(self.actionImportMaterialH)
        self.menuImport.addAction(self.actionImportDesign)
        self.menuDesign.addAction(self.actionDesign)
        self.menuDesign.addAction(self.actionLayerMaterial)
        self.menuDesign.addAction(self.actionSubstrate)
        self.menuD_eposition_settings.addAction(self.actionProcessParameters)
        self.menuD_eposition_settings.addAction(self.actionMainLog)
        self.menuD_eposition_settings.addAction(self.actionVacuumMachineSettings)
        self.menuD_eposition_settings.addAction(self.actionErrorPrevention)
        self.menu_Process_data.addAction(self.actionDataFitting)
        self.menu_Process_data.addAction(self.actionIterationExecutionTime)
        self.menu_Process_data.addAction(self.actionHistory)
        self.menu_Spectrometer.addAction(self.actionSpectrometerSettings)
        self.menu_Spectrometer.addAction(self.actionDataCorrection)
        self.menu_Spectrometer.addAction(self.actionRawData)
        self.menu_Options.addAction(self.actionSimulationParameters)
        self.menu_Options.addAction(self.actionReverseEngineering)
        self.toolBar.addAction(self.actionProjects)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSubstrate)
        self.toolBar.addAction(self.actionLayerMaterial)
        self.toolBar.addAction(self.actionDesign)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionProcessParameters)
        self.toolBar.addAction(self.actionDataFitting)
        self.toolBar.addAction(self.actionHistory)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionIterationExecutionTime)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSaveSpectra)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Monitor", None))
        self.actionProjects.setText(QCoreApplication.translate("MainWindow", u"&Projects...", None))
        self.actionSubstrate.setText(QCoreApplication.translate("MainWindow", u"&Substrate...", None))
        self.actionLayerMaterial.setText(QCoreApplication.translate("MainWindow", u"&Layer Material...", None))
        self.actionDesign.setText(QCoreApplication.translate("MainWindow", u"&Design...", None))
        self.actionProcessParameters.setText(QCoreApplication.translate("MainWindow", u"&Process Parameters...", None))
        self.actionDataFitting.setText(QCoreApplication.translate("MainWindow", u"&Data Fitting...", None))
        self.actionHistory.setText(QCoreApplication.translate("MainWindow", u"&History...", None))
        self.actionIterationExecutionTime.setText(QCoreApplication.translate("MainWindow", u"&Iteration Execution Time...", None))
        self.actionSaveSpectra.setText(QCoreApplication.translate("MainWindow", u"Save Spectra", None))
        self.actionSimulationParameters.setText(QCoreApplication.translate("MainWindow", u"&Simulation Parameters...", None))
        self.actionReverseEngineering.setText(QCoreApplication.translate("MainWindow", u"&Reverse Engineering...", None))
        self.actionSpectrometerSettings.setText(QCoreApplication.translate("MainWindow", u"&Spectrometer Settings...", None))
        self.actionDataCorrection.setText(QCoreApplication.translate("MainWindow", u"&Data Correction...", None))
        self.actionRawData.setText(QCoreApplication.translate("MainWindow", u"&Raw Data...", None))
        self.actionMainLog.setText(QCoreApplication.translate("MainWindow", u"&Main Log...", None))
        self.actionVacuumMachineSettings.setText(QCoreApplication.translate("MainWindow", u"&Vacuum Machine Settings...", None))
        self.actionErrorPrevention.setText(QCoreApplication.translate("MainWindow", u"&Error Prevention...", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"&New", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.actionImportSubstrate.setText(QCoreApplication.translate("MainWindow", u"Substrate...", None))
        self.actionImportMaterialL.setText(QCoreApplication.translate("MainWindow", u"Material L...", None))
        self.actionImportMaterialH.setText(QCoreApplication.translate("MainWindow", u"Material H...", None))
        self.actionImportDesign.setText(QCoreApplication.translate("MainWindow", u"Design...", None))
        self.groupBox_operations.setTitle("")
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonReset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.groupBox_information.setTitle("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Design th. (nm)::", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Current th. (nm):", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Value f_av:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Remaining th. (nm):", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Active layer:", None))
        self.labelRate.setText(QCoreApplication.translate("MainWindow", u"Rate (A/s):", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Execution t.:", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Material:", None))
        self.labelTotalLayers.setText(QCoreApplication.translate("MainWindow", u"Total layers:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Remaining time (s):", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuImport.setTitle(QCoreApplication.translate("MainWindow", u"Import", None))
        self.menuDesign.setTitle(QCoreApplication.translate("MainWindow", u"&Design", None))
        self.menuD_eposition_settings.setTitle(QCoreApplication.translate("MainWindow", u"D&eposition settings", None))
        self.menu_Process_data.setTitle(QCoreApplication.translate("MainWindow", u"&Process data", None))
        self.menu_Spectrometer.setTitle(QCoreApplication.translate("MainWindow", u"&Spectrometer", None))
        self.menu_Options.setTitle(QCoreApplication.translate("MainWindow", u"&Options", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

