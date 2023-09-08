from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout
from PySide6.QtCore import QMargins
from PySide6.QtCharts import QChart
from UI.SpectrometerDataCorrectionDialog_ui import Ui_SpectrometerDataCorrectionDialog
from Widgets.Dialogs.SpectrometerDataCorrectionDialog.SpectrometerDataCorrectionTableModel import (
    SpectrometerDataCorrectionTableModel,
)
from Widgets.ChartView.ChartView import ChartView


class SpectrometerDataCorrectionDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_SpectrometerDataCorrectionDialog()
        self.ui.setupUi(self)

        self.__init_chart()
        self.__init_chart_view()

        self.model = SpectrometerDataCorrectionTableModel(self)
        self.ui.tableView.setModel(self.model)

    def __init_chart(self):
        self.chart = QChart()
        self.chart.setMargins(QMargins())

    def __init_chart_view(self):
        self.chart_view = ChartView(self.chart)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(self.chart_view)

        self.ui.frameChart.setLayout(h_layout)
