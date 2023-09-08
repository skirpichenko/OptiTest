from PySide6.QtWidgets import QDialog, QWidget
from UI.MainLogDialog_ui import Ui_MainLogDialog


class MainLogDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainLogDialog()
        self.ui.setupUi(self)

        self.ui.plainTextEdit.appendPlainText("Log")