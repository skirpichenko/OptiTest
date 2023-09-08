from PySide6.QtCore import QObject, Signal
import numpy as np

from OptiReOpt.ReOpt import *
from OptiReOpt.VDP import *
from OptiReOpt.ORConstants import *

from Widgets.Dialogs.SimulationParametersDialog.SimulationParametersDialog import (
    SimulationParametersDialog,
)
import threading
import time


class ProjectManager(QObject):
    deposition_current_layer_index_changed = Signal()
    current_th_changed = Signal(float)
    rate_changed = Signal(float)
    rem_time_changed = Signal(float)
    f_avg_changed = Signal(float)
    execution_time_changed = Signal(float)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.reopt = ReOpt("test_characterization.log", 1)
        self.reopt.SetWavelengthGrid(np.arange(580, 780, 0.25, dtype=np.float64))
        self.reopt.lamMin = 580
        self.reopt.lamMax = 780
        self.reopt.config.rt_units = RTUnits.PERCENT

        self.vdp = VDP("test_simulation.log")
        self.vdp.d_currGeo = 0.  # TODO: just a quick workaroung, should be reimplemented
        self.vdp.rt_units = RTUnits.PERCENT
        self.vdp.SetFluctuations(0, 5, 1)
        self.vdp.noiseTR = 0.01

        self.deposition_thread = None
        self.deposition_current_layer_index = 0
        self._stop_event = threading.Event()

    def load_substrate(self, file_name: str):
        self.reopt.LoadMaterialFile("0", file_name)
        self.reopt.GetChip()
        self.reopt.onlineBackside = True
        self.reopt.onlineBacksideThickness = 1.2
        self.vdp.LoadChipFile("0", 1.2, file_name)

    def load_material_h(self, file_name: str):
        self.reopt.LoadMaterialFile("H", file_name)
        self.vdp.LoadMaterialFile("H", file_name)
        model = DepositionModel(
            LightUnits.ANGS.todef(3), LightUnits.ANGS.todef(0.3), 3, 0, True
        )
        self.vdp.LoadMaterialDeposition("H", model)

    def load_material_l(self, file_name: str):
        self.reopt.LoadMaterialFile("L", file_name)
        self.vdp.LoadMaterialFile("L", file_name)
        model = DepositionModel(
            LightUnits.ANGS.todef(3), LightUnits.ANGS.todef(0.3), 3, 0, True
        )
        self.vdp.LoadMaterialDeposition("L", model)

    def load_design(self, file_name: str):
        self.reopt.LoadTheoreticalDesignFile(file_name)

    def start_deposition(self, start: bool):
        if start:
            self._stop_event.clear()
            self.deposition_thread = threading.Thread(target=self.process_deposition)
            self.deposition_thread.start()
        else:
            self._stop_event.set()
            self.deposition_thread.join()
            self.deposition_thread = None

    def reset_deposition(self):
        self.vdp.ResetDeposition()
        self.deposition_current_layer_index = 0
        self.deposition_current_layer_index_changed.emit()

    def process_deposition(self):
        if self.reopt.design is None:
            return

        self.vdp.incidenceAngle = self.reopt.incidenceAngle
        self.vdp.hasBackSide = self.reopt.onlineBackside
        self.vdp.backSideThickness = self.reopt.onlineBacksideThickness
        self.vdp.pol = self.reopt.pol
        self.vdp.na = self.reopt.na

        while (
                not self._stop_event.is_set()
                and self.deposition_current_layer_index < self.reopt.design.nLayers
        ):
            abbr = self.reopt.design.layers[
                self.deposition_current_layer_index
            ].material.abbr
            self.vdp.StartDeposition("0", abbr)
            print(
                "Starting deposition of layer",
                self.deposition_current_layer_index + 1,
                "with material",
                abbr,
                "at time",
                self.vdp.tsecTotal,
            )
            nIter = 0
            tsec = 0  # this is the time since the beginning of the current layer deposition
            while not self._stop_event.is_set():
                nIter += 1
                self.vdp.IncreaseTime(SimulationParametersDialog.scan_interval)
                tsec += SimulationParametersDialog.scan_interval
                scan = self.vdp.GetScan(self.reopt.wavelength)

                start_time = (
                    time.time()
                )  # Get the current time before calling the function
                res = self.reopt.ProcessOnLineTRScan(
                    tm=tsec,
                    # this caused the problem. the time here has to be the time since the beginning of the current layer deposition, not the total time
                    lastLayer=self.deposition_current_layer_index + 1,
                    lam=self.reopt.wavelength,
                    val=scan,
                )
                end_time = (
                    time.time()
                )  # Get the current time after the function completes
                execution_time = end_time - start_time
                self.execution_time_changed.emit(execution_time)

                print(self.deposition_current_layer_index, nIter, tsec, res)
                self.current_th_changed.emit(res.d_currGeo)
                self.rate_changed.emit(res.v_dep)
                self.rem_time_changed.emit(res.dt_switch)
                self.f_avg_changed.emit(res.f_avg)

                with threading.Lock():
                    self.vdp.d_currGeo = res.d_currGeo

                if res.dt_switch < SimulationParametersDialog.scan_interval:
                    if res.dt_switch > 0:
                        self.vdp.IncreaseTime(res.dt_switch)
                    self.deposition_current_layer_index += 1
                    self.deposition_current_layer_index_changed.emit()
                    self.execution_time_changed.emit(0)
                    self.vdp.StopDeposition()
                    print("Switching to next layer")
                    break

                if SimulationParametersDialog.time_between_scans != -1:
                    time.sleep(
                        SimulationParametersDialog.scan_interval
                        / SimulationParametersDialog.time_between_scans
                    )
