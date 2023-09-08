from PySide6.QtWidgets import QDialog, QWidget
from UI.SpectrometerSettingsDialog_ui import Ui_SpectrometerSettingsDialog


class SpectrometerSettingsDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_SpectrometerSettingsDialog()
        self.ui.setupUi(self)
