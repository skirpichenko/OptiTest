from PySide6.QtCharts import QChartView, QChart, QValueAxis
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from typing import Optional


class ChartView(QChartView):
    def __init__(self, chart: QChart, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setChart(chart)
        self.setBackgroundBrush(chart.backgroundBrush())
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.__init_axes()

    def __init_axes(self):
        self.axis_x = QValueAxis()
        self.axis_x.setLabelFormat("%.2f")
        self.axis_x.setRange(0, 1000)
        self.chart().addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Transmittance [%]")
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setRange(0, 1000)
        self.chart().addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
