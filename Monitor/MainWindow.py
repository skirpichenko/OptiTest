from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog
from PySide6.QtCore import QMargins, Slot, Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtCharts import QChart, QLineSeries
from UI.MainWindow_ui import Ui_MainWindow
from Widgets.ChartView.ChartView import ChartView
from Widgets.Dialogs.ProjectsDialog.ProjectsDialog import ProjectsDialog
from Widgets.Dialogs.DatabaseDialog.DatabaseDialog import DatabaseDialog
from Widgets.Dialogs.ProcessParametersDialog.ProcessParametersDialog import (
    ProcessParametersDialog,
)
from Widgets.Dialogs.DataFittingDialog.DataFittingDialog import DataFittingDialog
from Widgets.Dialogs.HistoryDialog.HistoryDialog import HistoryDialog
from Widgets.Dialogs.IterationExecutionTimeDialog.IterationExecutionTimeDialog import (
    IterationExecutionTimeDialog,
)
from Widgets.Dialogs.SimulationParametersDialog.SimulationParametersDialog import (
    SimulationParametersDialog,
)
from Widgets.Dialogs.SpectrometerSettingsDialog.SpectrometerSettingsDialog import (
    SpectrometerSettingsDialog,
)
from Widgets.Dialogs.SpectrometerDataCorrectionDialog.SpectrometerDataCorrectionDialog import (
    SpectrometerDataCorrectionDialog,
)
from Widgets.Dialogs.MainLogDialog.MainLogDialog import MainLogDialog
from Widgets.Dialogs.ErrorPreventionDuringDepositionDialog.ErrorPreventionDuringDepositionDialog import (
    ErrorPreventionDuringDepositionDialog,
)
from Widgets.Dialogs.VacuumMachineSettngsDialog.VacuumMachineSettngsDialog import (
    VacuumMachineSettngsDialog,
)
from Widgets.Dialogs.RawDataDialog.RawDataDialog import RawDataDialog
from ProjectManager import ProjectManager
import numpy as np
import os


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__init_chart()
        self.__init_chart_view()
        self.__init_project_manager()
        self.__enable_buttons(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.draw_chart)

        self.load_existing_files()

    def __enable_buttons(self, enable: bool):
        self.ui.pushButtonStart.setEnabled(enable)
        self.ui.pushButtonReset.setEnabled(enable)

    def __init_project_manager(self):
        self.project_manager = ProjectManager(self)
        self.project_manager.deposition_current_layer_index_changed.connect(
            self.deposition_current_layer_index_changed
        )
        self.project_manager.current_th_changed.connect(self.current_th_changed)
        self.project_manager.rate_changed.connect(self.rate_changed)
        self.project_manager.rem_time_changed.connect(self.rem_time_changed)
        self.project_manager.f_avg_changed.connect(self.f_avg_changed)
        self.project_manager.execution_time_changed.connect(self.execution_time_changed)

    def deposition_current_layer_index_changed(self):
        index = self.project_manager.deposition_current_layer_index
        self.ui.lineEditActiveLayer.setText(str(index + 1))

        design = self.project_manager.reopt.design
        if design is None:
            return

        layers = self.project_manager.reopt.design.layers
        if layers is None:
            return

        if 0 <= index < len(layers):
            layer = layers[index]

            self.ui.lineEditDesignTh.setText("{:.3f}".format(layer.thickness))

            material = layer.material
            if not material is None:
                self.ui.lineEditMaterial.setText(material.airName)

    def current_th_changed(self, th):
        self.ui.lineEditCurrentTh.setText("{:.3f}".format(th))

        index = self.project_manager.deposition_current_layer_index
        design = self.project_manager.reopt.design
        if design is None:
            return

        layers = self.project_manager.reopt.design.layers
        if layers is None:
            return

        if 0 <= index < len(layers):
            layer = layers[index]
            self.ui.lineEditRemTh.setText("{:.3f}".format(layer.thickness - th))

    def rate_changed(self, value):
        self.ui.lineEditRate.setText("{:.3f}".format(value))

    def rem_time_changed(self, value):
        self.ui.lineEditRemTime.setText("{:.3f}".format(value))

    def f_avg_changed(self, value):
        self.ui.lineEditValueF_Av.setText("{:.3f}".format(value))

    def execution_time_changed(self, value):
        self.ui.lineEditExecutionT.setText("{:.3f}".format(value))

    def __init_chart(self):
        self.chart = QChart()
        self.chart.setMargins(QMargins())
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

    def __init_chart_view(self):
        self.chart_view = ChartView(self.chart)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(self.chart_view)

        self.ui.frame_chart.setLayout(h_layout)

    def __fill_ui_components(self):
        self.ui.lineEditDesignTh.setText(
            "{:.3f}".format(
                self.project_manager.reopt.design.layers[
                    self.project_manager.deposition_current_layer_index
                ].thickness
            )
        )
        self.ui.lineEditActiveLayer.setText(
            str(self.project_manager.deposition_current_layer_index + 1)
        )
        self.ui.lineEditTotalLayers.setText(
            str(self.project_manager.reopt.design.nLayers)
        )
        self.ui.lineEditMaterial.setText(
            self.project_manager.reopt.design.layers[
                self.project_manager.deposition_current_layer_index
            ].material.airName
        )

    def load_existing_files(self):
        file_path = os.getcwd() + "\\Monitor\\data\\substrate.out"
        if os.path.isfile(file_path):
            self.project_manager.load_substrate(file_path)

        file_path = os.getcwd() + "\\Monitor\\data\\H.out"
        if os.path.isfile(file_path):
            self.project_manager.load_material_h(file_path)

            file_path = os.getcwd() + "\\Monitor\\data\\L.out"
            if os.path.isfile(file_path):
                self.project_manager.load_material_l(file_path)

                file_path = os.getcwd() + "\\Monitor\\data\\design.out"
                if os.path.isfile(file_path):
                    self.project_manager.load_design(file_path)
                    self.__fill_ui_components()
                    self.__enable_buttons(True)
                    self.draw_chart()

    @Slot()
    def on_actionProjects_triggered(self):
        dlg = ProjectsDialog(self)
        dlg.exec()

    @Slot()
    def on_actionSubstrate_triggered(self):
        dlg = DatabaseDialog(
            self.project_manager.reopt, DatabaseDialog.TabRole.SUBSTRATE, self
        )
        dlg.exec()

    @Slot()
    def on_actionLayerMaterial_triggered(self):
        dlg = DatabaseDialog(
            self.project_manager.reopt, DatabaseDialog.TabRole.LAYERMATERIAL, self
        )
        dlg.exec()

    @Slot()
    def on_actionDesign_triggered(self):
        dlg = DatabaseDialog(
            self.project_manager.reopt, DatabaseDialog.TabRole.DESIGN, self
        )
        dlg.exec()

    @Slot()
    def on_actionProcessParameters_triggered(self):
        dlg = ProcessParametersDialog(self)
        dlg.exec()

    @Slot()
    def on_actionDataFitting_triggered(self):
        dlg = DataFittingDialog(self)
        dlg.exec()

    @Slot()
    def on_actionHistory_triggered(self):
        dlg = HistoryDialog(self)
        dlg.exec()

    @Slot()
    def on_actionIterationExecutionTime_triggered(self):
        dlg = IterationExecutionTimeDialog(self)
        dlg.exec()

    @Slot()
    def on_actionSimulationParameters_triggered(self):
        dlg = SimulationParametersDialog(
            self.project_manager.reopt, self.project_manager.vdp, self
        )
        dlg.exec()

    @Slot()
    def on_actionSpectrometerSettings_triggered(self):
        dlg = SpectrometerSettingsDialog(self)
        dlg.exec()

    @Slot()
    def on_actionDataCorrection_triggered(self):
        dlg = SpectrometerDataCorrectionDialog(self)
        dlg.exec()

    @Slot()
    def on_actionMainLog_triggered(self):
        dlg = MainLogDialog(self)
        dlg.exec()

    @Slot()
    def on_actionErrorPrevention_triggered(self):
        dlg = ErrorPreventionDuringDepositionDialog(self)
        dlg.exec()

    @Slot()
    def on_actionVacuumMachineSettings_triggered(self):
        dlg = VacuumMachineSettngsDialog(self)
        dlg.exec()

    @Slot()
    def on_actionRawData_triggered(self):
        dlg = RawDataDialog(self)
        dlg.exec()

    @Slot()
    def on_actionReverseEngineering_triggered(self):
        file_path = self.__open_file(
            "Import Data for Reverse Engineering",
            "Leybold Monitoring Report file (*.lmr);;Optical Design eXchange file (*.odx)",
        )

    @Slot()
    def on_actionNew_triggered(self):
        file_path = self.__open_file(
            "New Project",
            "Leybold Monitoring Report file (*.lmr);;Optical Design eXchange file (*.odx)",
        )

    @Slot()
    def on_actionImportSubstrate_triggered(self):
        file_path = self.__open_file(
            "Import Substrate",
            "OptiLayer Medium Report file (*.out)",
        )
        if file_path:
            self.project_manager.load_substrate(file_path)

    @Slot()
    def on_actionImportMaterialL_triggered(self):
        file_path = self.__open_file(
            "Import Material L",
            "OptiLayer Layer Material Report file (*.out)",
        )
        if file_path:
            self.project_manager.load_material_l(file_path)

    @Slot()
    def on_actionImportMaterialH_triggered(self):
        file_path = self.__open_file(
            "Import Material H",
            "OptiLayer Layer Material Report file (*.out)",
        )
        if file_path:
            self.project_manager.load_material_h(file_path)

    @Slot()
    def on_actionImportDesign_triggered(self):
        file_path = self.__open_file(
            "Import Design",
            "OptiLayer Design Report file (*.out)",
        )
        if file_path:
            self.project_manager.load_design(file_path)
            self.__fill_ui_components()
            self.__enable_buttons(True)
            self.draw_chart()

    def __open_file(self, caption, filter):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            caption,
            "",
            filter,
        )
        return file_path

    @Slot()
    def on_pushButtonReset_clicked(self):
        self.project_manager.reset_deposition()

    @Slot()
    def on_pushButtonStart_clicked(self):
        if self.ui.pushButtonStart.text() == "Start":
            self.ui.pushButtonStart.setText("Stop")
            self.ui.pushButtonReset.setEnabled(False)
            self.ui.actionSimulationParameters.setEnabled(False)
            self.project_manager.start_deposition(True)
        else:
            self.ui.pushButtonStart.setText("Start")
            self.ui.pushButtonReset.setEnabled(True)
            self.ui.actionSimulationParameters.setEnabled(True)
            self.project_manager.start_deposition(False)

    def draw_chart(self):
        self.chart.removeAllSeries()

        if self.project_manager.reopt.design is None:
            return

        wavelength = self.project_manager.reopt.wavelength
        scan = self.project_manager.vdp.GetScan(wavelength)

        reopt_incidenceAngle = self.project_manager.reopt.incidenceAngle
        reopt_pol = self.project_manager.reopt.pol
        reopt_dType = self.project_manager.vdp.rt_units

        # estimated
        th_bydesign = self.project_manager.reopt.design.layers[self.project_manager.deposition_current_layer_index].thickness
        th_estimated = self.project_manager.vdp.d_currGeo
        scanReOptFitting = self.project_manager.reopt.GetOnLineValues(
            wavelength,
            self.project_manager.deposition_current_layer_index + 1,
            th_estimated / th_bydesign,
            reopt_incidenceAngle,
            reopt_pol,
            reopt_dType,
        )

        scanReOptTheoretical = self.project_manager.reopt.GetOnLineValues(
            wavelength,
            self.project_manager.deposition_current_layer_index + 1,
            1,
            reopt_incidenceAngle,
            reopt_pol,
            reopt_dType,
        )
        scanReOptTheoretical_90 = self.project_manager.reopt.GetOnLineValues(
            wavelength,
            self.project_manager.deposition_current_layer_index + 1,
            0.9,
            reopt_incidenceAngle,
            reopt_pol,
            reopt_dType,
        )

        scanReOptTheoretical_80 = self.project_manager.reopt.GetOnLineValues(
            wavelength,
            self.project_manager.deposition_current_layer_index + 1,
            0.8,
            reopt_incidenceAngle,
            reopt_pol,
            reopt_dType,
        )

        spectra_series = QLineSeries(self.chart)
        spectra_series.setPen(QColor(Qt.GlobalColor.red))
        spectra_series.setName("Spectra")
        spectra_series.appendNp(wavelength, scan)
        self.chart.addSeries(spectra_series)
        spectra_series.attachAxis(self.chart_view.axis_x)
        spectra_series.attachAxis(self.chart_view.axis_y)

        theoretical_series = QLineSeries(self.chart)
        theoretical_series.setName("Line 100%")
        theoretical_series.appendNp(wavelength, scanReOptTheoretical)
        self.chart.addSeries(theoretical_series)
        theoretical_series.attachAxis(self.chart_view.axis_x)
        theoretical_series.attachAxis(self.chart_view.axis_y)

        theoretical_series_90 = QLineSeries(self.chart)
        theoretical_series_90.setPen(QColor(Qt.GlobalColor.blue))
        theoretical_series_90.setName("Line 90%")
        theoretical_series_90.appendNp(wavelength, scanReOptTheoretical_90)
        self.chart.addSeries(theoretical_series_90)
        theoretical_series_90.attachAxis(self.chart_view.axis_x)
        theoretical_series_90.attachAxis(self.chart_view.axis_y)

        theoretical_series_80 = QLineSeries(self.chart)
        theoretical_series_80.setPen(QColor(Qt.GlobalColor.yellow))
        theoretical_series_80.setName("Line 80%")
        theoretical_series_80.appendNp(wavelength, scanReOptTheoretical_80)
        self.chart.addSeries(theoretical_series_80)
        theoretical_series_80.attachAxis(self.chart_view.axis_x)
        theoretical_series_80.attachAxis(self.chart_view.axis_y)


        fitting = QLineSeries(self.chart)
        fitting.setPen(QColor(Qt.GlobalColor.cyan))
        fitting.setName("Fitting")
        fitting.appendNp(wavelength, scanReOptFitting)
        self.chart.addSeries(fitting)
        fitting.attachAxis(self.chart_view.axis_x)
        fitting.attachAxis(self.chart_view.axis_y)

        self.chart_view.axis_x.setRange(np.min(wavelength), np.max(wavelength))
        self.chart_view.axis_y.setRange(0, 100)

        self.chart_view.axis_x.applyNiceNumbers()
        self.chart_view.axis_y.applyNiceNumbers()
        self.chart.update()

        self.timer.start(1000)
