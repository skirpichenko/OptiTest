from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QAbstractItemView
from PySide6.QtCore import QMargins, QItemSelectionModel, QItemSelection
from PySide6.QtCharts import QChart, QLineSeries
from UI.DatabaseDialog_ui import Ui_DatabaseDialog
from Widgets.Dialogs.DatabaseDialog.DatabaseSubstrateTableModel import (
    DatabaseSubstrateTableModel,
)
from Widgets.Dialogs.DatabaseDialog.DatabaseLayerMaterialTableModel import (
    DatabaseLayerMaterialTableModel,
)
from Widgets.Dialogs.DatabaseDialog.DatabaseDesignTableModel import (
    DatabaseDesignTableModel,
)
from Widgets.Dialogs.DatabaseDialog.DatabaseRefractiveIndexTableModel import (
    DatabaseRefractiveIndexTableModel,
)
from enum import IntEnum
from Widgets.ChartView.ChartView import ChartView
import numpy as np


class DatabaseDialog(QDialog):
    class TabRole(IntEnum):
        SUBSTRATE = 0
        LAYERMATERIAL = 1
        DESIGN = 2

    def __init__(self, reopt, tab_role: TabRole, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_DatabaseDialog()
        self.ui.setupUi(self)
        self.reopt = reopt

        match tab_role:
            case DatabaseDialog.TabRole.SUBSTRATE:
                self.ui.tabWidget.setCurrentIndex(0)
            case DatabaseDialog.TabRole.LAYERMATERIAL:
                self.ui.tabWidget.setCurrentIndex(1)
            case DatabaseDialog.TabRole.DESIGN:
                self.ui.tabWidget.setCurrentIndex(2)

        self.ui.tableViewSubstrate.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.ui.tableViewSubstrate.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.substrate_model = DatabaseSubstrateTableModel(reopt, self)
        self.ui.tableViewSubstrate.setModel(self.substrate_model)
        self.substrate_sel_model = QItemSelectionModel(self.substrate_model, self)
        self.ui.tableViewSubstrate.setSelectionModel(self.substrate_sel_model)
        self.substrate_sel_model.selectionChanged.connect(
            self.on_substrate_sel_model_selectionChanged
        )

        self.ui.tableViewLayerMaterial.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.ui.tableViewLayerMaterial.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.layer_material_model = DatabaseLayerMaterialTableModel(reopt, self)
        self.ui.tableViewLayerMaterial.setModel(self.layer_material_model)
        self.layer_material_sel_model = QItemSelectionModel(
            self.layer_material_model, self
        )
        self.ui.tableViewLayerMaterial.setSelectionModel(self.layer_material_sel_model)
        self.layer_material_sel_model.selectionChanged.connect(
            self.on_layer_material_sel_model_selectionChanged
        )

        self.design_model = DatabaseDesignTableModel(reopt, self)
        self.ui.tableViewDesign.setModel(self.design_model)

        self.substrate_refractive_index_model = DatabaseRefractiveIndexTableModel(self)
        self.ui.tableViewSubstrateMaterial.setModel(
            self.substrate_refractive_index_model
        )

        self.layer_material_refractive_index_model = DatabaseRefractiveIndexTableModel(
            self
        )
        self.ui.tableViewLayerMaterialMaterial.setModel(
            self.layer_material_refractive_index_model
        )

        if not self.reopt is None:
            self.ui.lineEditNumberOfLayers.setText(str(self.reopt.nLayers))
            self.ui.lineEditAngelOfIncidence.setText(str(self.reopt.incidenceAngle))
            if not self.reopt.design is None:
                self.ui.lineEditDesignWavelength.setText(str(self.reopt.design.controlW))
                self.ui.lineEditInputMedium.setText(str(self.reopt.design.matchMedium))

        self.substrate_chart = QChart()
        self.substrate_chart_view = ChartView(self.substrate_chart)
        self.substrate_chart_view.chart().setMargins(QMargins())
        self.substrate_chart_view.axis_y.setTitleText("Refractive Index")
        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(self.substrate_chart_view)
        self.ui.tabPlotSubstrate.setLayout(hLayout)

        self.layer_material_chart = QChart()
        self.layer_material_chart_view = ChartView(self.layer_material_chart)
        self.layer_material_chart_view.chart().setMargins(QMargins())
        self.layer_material_chart_view.axis_y.setTitleText("Refractive Index")
        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(self.layer_material_chart_view)
        self.ui.tabPlotLayerMaterial.setLayout(hLayout)

        self.__select_first_row()

    def __select_first_row(self):
        if self.substrate_model.rowCount() > 0:
            self.substrate_sel_model.select(
                QItemSelection(
                    self.substrate_model.index(0, 0),
                    self.substrate_model.index(0, 1),
                ),
                QItemSelectionModel.SelectionFlag.Select,
            )

        if self.layer_material_model.rowCount() > 0:
            self.layer_material_sel_model.select(
                QItemSelection(
                    self.layer_material_model.index(0, 0),
                    self.layer_material_model.index(0, 1),
                ),
                QItemSelectionModel.SelectionFlag.Select,
            )

    def on_substrate_sel_model_selectionChanged(self):
        self.substrate_chart.removeAllSeries()
        rows = self.substrate_sel_model.selectedRows()
        if len(rows) == 0:
            self.substrate_refractive_index_model.set_refractive_index(None)
            return
        chip = list(self.reopt.name2chip.values())[rows[0].row()]
        refractive_index = chip.substrate.material.riAir
        self.substrate_refractive_index_model.set_refractive_index(refractive_index)

        # init chart
        n_series = QLineSeries(self.substrate_chart)
        n_series.setName("n")
        n_series.appendNp(refractive_index.wavelength, refractive_index.n)
        self.substrate_chart.addSeries(n_series)
        n_series.attachAxis(self.substrate_chart_view.axis_x)
        n_series.attachAxis(self.substrate_chart_view.axis_y)

        k_series = QLineSeries(self.substrate_chart)
        k_series.setName("k")
        k_series.appendNp(refractive_index.wavelength, refractive_index.k)
        self.substrate_chart.addSeries(k_series)
        k_series.attachAxis(self.substrate_chart_view.axis_x)
        k_series.attachAxis(self.substrate_chart_view.axis_y)

        self.substrate_chart_view.axis_x.setRange(
            np.min(refractive_index.wavelength), np.max(refractive_index.wavelength)
        )
        self.substrate_chart_view.axis_y.setRange(
            min(np.min(refractive_index.n), np.min(refractive_index.k)),
            max(np.max(refractive_index.n), np.max(refractive_index.k)),
        )

        self.substrate_chart_view.axis_x.applyNiceNumbers()
        self.substrate_chart_view.axis_y.applyNiceNumbers()
        self.substrate_chart.update()

    def on_layer_material_sel_model_selectionChanged(self):
        self.layer_material_chart.removeAllSeries()
        rows = self.layer_material_sel_model.selectedRows()
        if len(rows) == 0:
            self.layer_material_refractive_index_model.set_refractive_index(None)
            return
        material = list([v for k,v in self.reopt.abbr2material.items() if k != "0"])[rows[0].row()]
        refractive_index = material.riAir
        self.layer_material_refractive_index_model.set_refractive_index(
            refractive_index
        )

        # init chart
        n_series = QLineSeries(self.layer_material_chart)
        n_series.setName("n")
        n_series.appendNp(refractive_index.wavelength, refractive_index.n)
        self.layer_material_chart.addSeries(n_series)
        n_series.attachAxis(self.layer_material_chart_view.axis_x)
        n_series.attachAxis(self.layer_material_chart_view.axis_y)

        k_series = QLineSeries(self.layer_material_chart)
        k_series.setName("k")
        k_series.appendNp(refractive_index.wavelength, refractive_index.k)
        self.layer_material_chart.addSeries(k_series)
        k_series.attachAxis(self.layer_material_chart_view.axis_x)
        k_series.attachAxis(self.layer_material_chart_view.axis_y)

        self.layer_material_chart_view.axis_x.setRange(
            np.min(refractive_index.wavelength), np.max(refractive_index.wavelength)
        )
        self.layer_material_chart_view.axis_y.setRange(
            min(np.min(refractive_index.n), np.min(refractive_index.k)),
            max(np.max(refractive_index.n), np.max(refractive_index.k)),
        )

        self.layer_material_chart_view.axis_x.applyNiceNumbers()
        self.layer_material_chart_view.axis_y.applyNiceNumbers()
        self.layer_material_chart.update()
