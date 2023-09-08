from PySide6.QtWidgets import QDialog, QWidget
from UI.ErrorPreventionDuringDepositionDialog_ui import (
    Ui_ErrorPreventionDuringDepositionDialog,
)


class ErrorPreventionDuringDepositionDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ErrorPreventionDuringDepositionDialog()
        self.ui.setupUi(self)
