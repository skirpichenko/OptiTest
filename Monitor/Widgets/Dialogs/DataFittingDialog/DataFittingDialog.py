from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QStackedWidget,
    QTabBar,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import QMargins
from PySide6.QtCharts import QChart
from Widgets.ChartView.ChartView import ChartView
from UI.DataFittingDialog_ui import Ui_DataFittingDialog
from Widgets.Dialogs.DataFittingDialog.DataFittingDialogThicknessesTableModel import (
    DataFittingDialogThicknessesTableModel,
)


class DataFittingDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_DataFittingDialog()
        self.ui.setupUi(self)

        self.__init_tabSpectralDataFitting()
        self.__init_tabThicknesses()
        self.__init_tabRatesChart()

    def __init_tabSpectralDataFitting(self):
        self.tab_spectral_stacked_widget = QStackedWidget()

        self.tab_spectral_tab_bar = QTabBar()
        self.tab_spectral_tab_bar.setExpanding(False)
        self.tab_spectral_tab_bar.setShape(QTabBar.Shape.RoundedSouth)

        self.export_button = QPushButton("Export to Excel")
        self.export_button.setAutoDefault(False)

        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(self.tab_spectral_tab_bar)
        hLayout.addWidget(self.export_button)
        hLayout.setStretch(0, 255)
        hLayout.setStretch(1, 1)

        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        vLayout.addWidget(self.tab_spectral_stacked_widget)
        vLayout.addLayout(hLayout)

        self.ui.tabSpectralDataFitting.setLayout(vLayout)

        self.__create_spectral_chart_view("1")
        self.__create_spectral_chart_view("2")
        self.__create_spectral_chart_view("3")
        self.__create_spectral_chart_view("4")

    def __create_spectral_chart_view(self, title: str):
        chart_view = ChartView(QChart())
        chart_view.chart().setMargins(QMargins())
        self.tab_spectral_stacked_widget.addWidget(chart_view)
        self.tab_spectral_tab_bar.addTab(title)

    def __init_tabThicknesses(self):
        self.__init_tabThicknessesRelativeErrors()
        self.__init_tabThicknessesAbsoluteErrors()
        self.__init_tabThicknessesTable()

    def __init_tabThicknessesRelativeErrors(self):
        chart_view = ChartView(QChart())
        chart_view.chart().setMargins(QMargins())
        chart_view.axis_y.setTitleText("Relative Errors [%]")
        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(chart_view)
        self.ui.tabRelativeErrors.setLayout(hLayout)

    def __init_tabThicknessesAbsoluteErrors(self):
        chart_view = ChartView(QChart())
        chart_view.chart().setMargins(QMargins())
        chart_view.axis_y.setTitleText("Absolute Errors [nm]")
        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(chart_view)
        self.ui.tabAbsoluteErrors.setLayout(hLayout)

    def __init_tabThicknessesTable(self):
        self.thickness_model = DataFittingDialogThicknessesTableModel(self)
        self.ui.thicknessTableView.setModel(self.thickness_model)
        self.ui.thicknessTableView.horizontalHeader().setStretchLastSection(True)

    def __init_tabRatesChart(self):
        self.tab_rates_stacked_widget = QStackedWidget()

        self.tab_rates_tab_bar = QTabBar()
        self.tab_rates_tab_bar.setExpanding(False)
        self.tab_rates_tab_bar.setShape(QTabBar.Shape.RoundedSouth)

        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        vLayout.addWidget(self.tab_rates_stacked_widget)
        vLayout.addWidget(self.tab_rates_tab_bar)

        self.ui.tabRatesChart.setLayout(vLayout)

        self.__create_rates_chart_view("1")
        self.__create_rates_chart_view("2")
        self.__create_rates_chart_view("3")
        self.__create_rates_chart_view("4")

    def __create_rates_chart_view(self, title: str):
        chart_view = ChartView(QChart())
        chart_view.chart().setMargins(QMargins())
        self.tab_rates_stacked_widget.addWidget(chart_view)
        self.tab_rates_tab_bar.addTab(title)
