from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtCore import Slot, QSignalBlocker
from UI.SimulationParametersDialog_ui import Ui_SimulationParametersDialog
from Widgets.Dialogs.SimulationParametersDialog.SimulationParametersTableModel import (
    SimulationParametersTableModel,
)
import sys
from Widgets.Dialogs.SimulationParametersDialog.SimulationParametersDoubleDelegate import (
    SimulationParametersDoubleDelegate,
)

from OptiReOpt.ORConstants import *


class SimulationParametersDialog(QDialog):
    scan_interval = 2
    time_between_scans = 16

    def __init__(self, reopt, vdp, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_SimulationParametersDialog()
        self.ui.setupUi(self)

        self.reopt = reopt
        self.vdp = vdp

        # set model
        self.model = SimulationParametersTableModel(vdp, self)
        self.ui.tableView.setModel(self.model)

        # set column delegate
        self.ui.tableView.setItemDelegateForColumn(
            1, SimulationParametersDoubleDelegate(self)
        )
        self.ui.tableView.setItemDelegateForColumn(
            2, SimulationParametersDoubleDelegate(self)
        )
        self.ui.tableView.setItemDelegateForColumn(
            3, SimulationParametersDoubleDelegate(self)
        )

        # set max range
        max_double = sys.float_info.max
        self.ui.doubleSpinBoxWavelengthLimitsLower.setMaximum(max_double)
        self.ui.doubleSpinBoxWavelengthLimitsUpper.setMaximum(max_double)
        self.ui.doubleSpinBoxMeanShutterDelay.setMaximum(max_double)
        self.ui.doubleSpinBoxShutterDelayRMS.setMaximum(max_double)
        self.ui.doubleSpinBoxFluktuationsMeanTime.setMaximum(max_double)
        self.ui.doubleSpinBoxFluktuationsRMS.setMaximum(max_double)
        self.ui.doubleSpinBoxCalibrationDriftsRate.setMaximum(max_double)
        self.ui.doubleSpinBoxCalibrationDriftsRecalibrTime.setMaximum(max_double)
        self.ui.doubleSpinBoxScanInterval.setMaximum(max_double)
        self.ui.doubleSpinBoxThOfTheSubstrate.setMaximum(max_double)

        # set default values
        self.ui.doubleSpinBoxMeanShutterDelay.setValue(0)
        self.ui.doubleSpinBoxShutterDelayRMS.setValue(0)
        self.ui.doubleSpinBoxScanInterval.setValue(
            SimulationParametersDialog.scan_interval
        )

        if not self.vdp is None:
            if not self.vdp.name2chip is None:
                if "0" in self.vdp.name2chip:
                    substrate = self.vdp.name2chip["0"].substrate
                    if not substrate is None:
                        if not substrate.thickness is None:
                            self.ui.doubleSpinBoxThOfTheSubstrate.setValue(
                                substrate.thickness
                            )

            if not self.vdp.incidenceAngle is None:
                self.ui.doubleSpinBoxAngleOfIncidence.setValue(self.vdp.incidenceAngle)
            if not self.vdp.calibrDriftRate is None:
                self.ui.doubleSpinBoxCalibrationDriftsRate.setValue(
                    self.vdp.calibrDriftRate
                )
            if not self.vdp.recalibrTime is None:
                self.ui.doubleSpinBoxCalibrationDriftsRecalibrTime.setValue(
                    self.vdp.recalibrTime
                )

            if not self.vdp.levelFluct is None:
                if not self.vdp.levelFluct.std is None:
                    self.ui.doubleSpinBoxFluktuationsDrift.setValue(
                        self.vdp.levelFluct.std
                    )
                if not self.vdp.levelFluct.meanTime is None:
                    self.ui.doubleSpinBoxFluktuationsMeanTime.setValue(
                        self.vdp.levelFluct.meanTime
                    )
                if not self.vdp.levelFluct.stdTime is None:
                    self.ui.doubleSpinBoxFluktuationsRMS.setValue(
                        self.vdp.levelFluct.stdTime
                    )
            if not self.vdp.noiseTR is None:
                self.ui.doubleSpinBoxRandomErrors.setValue(self.vdp.noiseTR)

            if not self.vdp.pol is None:
                match self.vdp.pol.value:
                    case 1:
                        self.ui.radioButtonPOL_S.setChecked(True)
                    case 2:
                        self.ui.radioButtonPOL_P.setChecked(True)
                    case 3:
                        self.ui.radioButtonPOL_A.setChecked(True)

            if not self.vdp.rt_data is None:
                match self.vdp.rt_data.value:
                    case 1:
                        self.ui.radioButtonInputData_Reflectance.setChecked(True)
                    case 2:
                        self.ui.radioButtonInputData_Transmittance.setChecked(True)

        if not self.reopt is None:
            if not self.reopt.lamMin is None:
                self.ui.doubleSpinBoxWavelengthLimitsLower.setValue(self.reopt.lamMin)
            if not self.reopt.lamMax is None:
                self.ui.doubleSpinBoxWavelengthLimitsUpper.setValue(self.reopt.lamMax)

            if not self.reopt.config is None:
                if not self.reopt.config.dataCorr is None:
                    match self.reopt.config.dataCorr.value:
                        case 0:
                            self.ui.groupBoxRefining.setEnabled(False)
                            self.ui.radioButtonRefiningLastLayer.setChecked(False)
                            self.ui.radioButtonRefiningAllLayers.setChecked(False)
                        case 1:
                            self.ui.groupBoxRefining.setEnabled(True)
                            self.ui.radioButtonRefiningLastLayer.setChecked(True)
                        case 2:
                            self.ui.groupBoxRefining.setEnabled(True)
                            self.ui.radioButtonRefiningAllLayers.setChecked(True)
                if not self.reopt.config.dataCorrType is None:
                    match self.reopt.config.dataCorrType.value:
                        case 1:
                            self.ui.radioButtonInputDataShift_Shift.setChecked(True)
                        case 2:
                            self.ui.radioButtonInputDataShift_Scale.setChecked(True)

        block = QSignalBlocker(self.ui.comboBoxTimeBetweenScans)
        self.ui.comboBoxTimeBetweenScans.clear()
        self.ui.comboBoxTimeBetweenScans.addItem("Normal", 1)
        self.ui.comboBoxTimeBetweenScans.addItem("Normal/2", 2)
        self.ui.comboBoxTimeBetweenScans.addItem("Normal/4", 4)
        self.ui.comboBoxTimeBetweenScans.addItem("Normal/8", 8)
        self.ui.comboBoxTimeBetweenScans.addItem("Normal/16", 16)
        self.ui.comboBoxTimeBetweenScans.addItem("Normal/32", 32)
        self.ui.comboBoxTimeBetweenScans.addItem("No delay (maximum prefix)", -1)
        index = self.ui.comboBoxTimeBetweenScans.findData(
            SimulationParametersDialog.time_between_scans
        )
        if index != -1:
            self.ui.comboBoxTimeBetweenScans.setCurrentIndex(index)
        else:
            self.ui.comboBoxTimeBetweenScans.setCurrentIndex(0)
        block.unblock()

    @Slot(float)
    def on_doubleSpinBoxWavelengthLimitsLower_valueChanged(self, value):
        if self.reopt is not None:
            self.reopt.lamMin = value

    @Slot(float)
    def on_doubleSpinBoxWavelengthLimitsUpper_valueChanged(self, value):
        if self.reopt is not None:
            self.reopt.lamMax = value

    @Slot(float)
    def on_doubleSpinBoxRandomErrors_valueChanged(self, value):
        if self.vdp is not None:
            self.vdp.noiseTR = value

    @Slot(float)
    def on_doubleSpinBoxMeanShutterDelay_valueChanged(self, value):
        pass

    @Slot(float)
    def on_doubleSpinBoxShutterDelayRMS_valueChanged(self, value):
        pass

    @Slot(float)
    def on_doubleSpinBoxFluktuationsDrift_valueChanged(self, value):
        if self.vdp is not None and self.vdp.levelFluct is not None:
            self.vdp.levelFluct.std = value

    @Slot(float)
    def on_doubleSpinBoxFluktuationsMeanTime_valueChanged(self, value):
        if self.vdp is not None and self.vdp.levelFluct is not None:
            self.vdp.levelFluct.meanTime = value

    @Slot(float)
    def on_doubleSpinBoxFluktuationsRMS_valueChanged(self, value):
        if self.vdp is not None and self.vdp.levelFluct is not None:
            self.vdp.levelFluct.stdTime = value

    @Slot(float)
    def on_doubleSpinBoxCalibrationDriftsRate_valueChanged(self, value):
        if self.vdp is not None:
            self.vdp.calibrDriftRate = value

    @Slot(float)
    def on_doubleSpinBoxCalibrationDriftsRecalibrTime_valueChanged(self, value):
        if self.vdp is not None:
            self.vdp.recalibrTime = value

    @Slot(float)
    def on_doubleSpinBoxAngleOfIncidence_valueChanged(self, value):
        if self.vdp is not None:
            self.vdp.incidenceAngle = value

    @Slot(float)
    def on_doubleSpinBoxScanInterval_valueChanged(self, value):
        SimulationParametersDialog.scan_interval = value

    @Slot(float)
    def on_doubleSpinBoxThOfTheSubstrate_valueChanged(self, value):
        key = "0"
        if (
            self.vdp is not None
            and self.vdp.name2chip is not None
            and key in self.vdp.name2chip
            and self.vdp.name2chip[key].substrate is not None
        ):
            self.vdp.name2chip[key].substrate.thickness = value

        if self.reopt is not None:
            self.reopt.onlineBacksideThickness = value

    @Slot(bool)
    def on_radioButtonRefiningLastLayer_clicked(self, checked):
        if self.reopt is not None and self.reopt.config is not None:
            self.reopt.config.dataCorr = InputDataCorrection.LAST_ONLY

    @Slot(bool)
    def on_radioButtonRefiningAllLayers_clicked(self, checked):
        if self.reopt is not None and self.reopt.config is not None:
            self.reopt.config.dataCorr = InputDataCorrection.ALL_SCANS

    @Slot(bool)
    def on_radioButtonPOL_S_clicked(self, checked):
        if self.vdp is not None:
            self.vdp.pol = Polarization.S

    @Slot(bool)
    def on_radioButtonPOL_P_clicked(self, checked):
        if self.vdp is not None:
            self.vdp.pol = Polarization.P

    @Slot(bool)
    def on_radioButtonPOL_A_clicked(self, checked):
        if self.vdp is not None:
            self.vdp.pol = Polarization.A

    @Slot(bool)
    def on_radioButtonInputData_Transmittance_clicked(self, checked):
        if self.vdp is not None:
            self.vdp.rt_data = DataType.TRANS

    @Slot(bool)
    def on_radioButtonInputData_Reflectance_clicked(self, checked):
        if self.vdp is not None:
            self.vdp.rt_data = DataType.REFL

    @Slot(bool)
    def on_radioButtonInputDataShift_Shift_clicked(self, checked):
        if self.reopt is not None and self.reopt.config is not None:
            self.reopt.config.dataCorrType = InputDataCorrectionMethod.SHIFT

    @Slot(bool)
    def on_radioButtonInputDataShift_Scale_clicked(self, checked):
        if self.reopt is not None and self.reopt.config is not None:
            self.reopt.config.dataCorrType = InputDataCorrectionMethod.SCALE

    @Slot(int)
    def on_comboBoxTimeBetweenScans_currentIndexChanged(self, index):
        SimulationParametersDialog.time_between_scans = (
            self.ui.comboBoxTimeBetweenScans.itemData(index)
        )
