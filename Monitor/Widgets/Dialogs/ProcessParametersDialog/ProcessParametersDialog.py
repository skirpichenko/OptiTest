from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtGui import QShowEvent
from UI.ProcessParametersDialog_ui import Ui_ProcessParametersDialog


class ProcessParametersDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ProcessParametersDialog()
        self.ui.setupUi(self)

    def showEvent(self, arg__1: QShowEvent) -> None:
        super().showEvent(arg__1)
        self.ui.groupBoxPalarizationState.setMinimumWidth(
            self.ui.groupBoxRefining.width()
        )
