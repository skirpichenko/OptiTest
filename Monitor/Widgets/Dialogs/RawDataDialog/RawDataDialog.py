from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout
from UI.RawDataDialog_ui import Ui_RawDataDialog
from PySide6.QtCore import QMargins
from PySide6.QtCharts import QChart
from Widgets.ChartView.ChartView import ChartView


class RawDataDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_RawDataDialog()
        self.ui.setupUi(self)

        self.__init_chart_view()

    def __init_chart_view(self):
        self.chart = QChart()
        self.chart.setMargins(QMargins())
        chart_view = ChartView(self.chart)
        chart_view.axis_y.setTitleText("Intensity [0-65536]")
        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(chart_view)
        self.ui.frameChartView.setLayout(hLayout)
